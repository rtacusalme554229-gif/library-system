from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter

from datetime import datetime, date

from models.user_model import UserModel
from models.book_model import BookModel
from models.borrow_model import BorrowModel

from views.manage_members_view import ManageMembersView
from views.reports_view import ReportsView
from views.admin_inventory_view import AdminInventoryView
from views.create_librarian_popup_view import CreateLibrarianPopupView


class AdminController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.admin_dashboard = None
        self.manage_members_view = None
        self.reports_view = None
        self.admin_inventory_view = None
        self.create_librarian_popup = None

    def set_dashboard(self, dashboard):
        self.admin_dashboard = dashboard
        self.refresh_dashboard_stats()

    # ================= DASHBOARD =================

    def refresh_dashboard_stats(self):
        if not self.admin_dashboard:
            return

        total_books = BookModel.count_all_books()
        available_books = BookModel.count_available_books()
        borrowed_books = BookModel.count_borrowed_books()

        total_users = UserModel.count_users_by_role("student")
        total_librarians = UserModel.count_users_by_role("librarian")
        total_members = total_users + total_librarians

        self.admin_dashboard.set_stats(
            total_books,
            available_books,
            borrowed_books,
            total_members
        )

        records = BorrowModel.get_all_borrow_records()
        today = date.today()

        active_borrowed = 0
        overdue_records = []
        total_penalty = 0
        book_counter = {}

        for record in records:
            penalty = float(record["penalty"]) if record["penalty"] else 0
            total_penalty += penalty

            book_title = record["book_title"]
            book_counter[book_title] = book_counter.get(book_title, 0) + 1

            if record["status"] == "Borrowed":
                active_borrowed += 1

                due_date = record["due_date"]

                if hasattr(due_date, "date"):
                    due_date = due_date.date()

                if due_date < today:
                    late_days = (today - due_date).days

                    overdue_records.append({
                        "id": record["id"],
                        "student_name": record["student_name"],
                        "book_title": record["book_title"],
                        "borrow_date": record["borrow_date"],
                        "due_date": due_date,
                        "late_days": late_days,
                        "status": record["status"],
                        "penalty": record["penalty"]
                    })

        most_borrowed = max(book_counter, key=book_counter.get) if book_counter else "-"

        if hasattr(self.admin_dashboard, "set_insights"):
            self.admin_dashboard.set_insights(
                most_borrowed,
                active_borrowed,
                len(overdue_records),
                total_penalty
            )

        if hasattr(self.admin_dashboard, "set_overdue_books"):
            self.admin_dashboard.set_overdue_books(overdue_records)

    def logout(self):
        self.auth_controller.logout()

    # ================= MANAGE ACCOUNTS =================

    def open_manage_members(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.manage_members_view = ManageMembersView(self)
        self.manage_members_view.show()
        self.load_members("librarian")

    def open_create_librarian(self):
        self.open_create_librarian_popup()

    def open_create_librarian_popup(self):
        self.create_librarian_popup = CreateLibrarianPopupView(self)
        self.create_librarian_popup.show()

    def save_librarian(self):
        view = self.create_librarian_popup

        if not view:
            return

        first_name = view.first_name_input.text().strip()
        last_name = view.last_name_input.text().strip()
        email = view.email_input.text().strip()
        address = view.address_input.text().strip()
        password = view.password_input.text().strip()

        if not all([first_name, last_name, email, address, password]):
            view.show_error("Error", "Please fill in all fields.")
            return

        existing_user = UserModel.find_by_email(email)

        if existing_user:
            view.show_error("Error", "Email already exists.")
            return

        librarian_id = UserModel.create_librarian(
            first_name,
            last_name,
            email,
            address,
            password
        )

        if librarian_id:
            view.show_message(
                "Success",
                "Librarian account created successfully."
            )

            view.close()
            self.create_librarian_popup = None

            if self.manage_members_view:
                self.load_members("librarian")

            self.refresh_dashboard_stats()
        else:
            view.show_error(
                "Error",
                "Failed to create librarian account."
            )

    def load_members(self, role):
        users = UserModel.get_users_by_role(role)

        if self.manage_members_view:
            self.manage_members_view.populate_table(users, role)

    def update_selected_account(self):
        view = self.manage_members_view

        if not view:
            return

        if not view.selected_user_id:
            view.show_error("Error", "Please select an account first.")
            return

        user_id = view.selected_user_id
        new_status = view.status_combo.currentText()

        # USERS TAB: update status only
        if view.current_role == "student":
            success = UserModel.update_user_status(user_id, new_status)

            if success:
                view.show_message(
                    "Success",
                    f"User status updated to {new_status}."
                )
                self.load_members("student")
                self.refresh_dashboard_stats()
            else:
                view.show_error("Error", "Failed to update user status.")

            return

        # LIBRARIANS TAB: update info + status
        first_name = view.first_name_input.text().strip()
        last_name = view.last_name_input.text().strip()
        email = view.email_input.text().strip()
        address = view.address_input.text().strip()

        if not all([first_name, last_name, email, address]):
            view.show_error("Error", "Please fill in all librarian details.")
            return

        existing_user = UserModel.find_by_email(email)

        if existing_user and existing_user["id"] != user_id:
            view.show_error("Error", "Email already exists.")
            return

        info_success = UserModel.update_librarian(
            user_id,
            first_name,
            last_name,
            email,
            address
        )

        status_success = UserModel.update_user_status(user_id, new_status)

        if info_success and status_success:
            view.show_message(
                "Success",
                "Librarian account updated successfully."
            )
            view.clear_edit_form()
            self.load_members("librarian")
            self.refresh_dashboard_stats()
        else:
            view.show_error("Error", "Failed to update librarian account.")

    def delete_selected_account(self):
        view = self.manage_members_view

        if not view:
            return

        if not view.selected_user_id:
            view.show_error("Error", "Please select an account first.")
            return

        user_id = view.selected_user_id

        if view.current_role == "student":
            view.show_error(
                "Not Allowed",
                "Users cannot be deleted from the Admin Manage Accounts page. Use status Inactive instead."
            )
            return

        reply = QMessageBox.question(
            view,
            "Confirm Delete",
            "Are you sure you want to delete this librarian account?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = UserModel.delete_librarian(user_id)

            if success:
                view.show_message(
                    "Success",
                    "Librarian account deleted successfully."
                )
                view.clear_edit_form()
                self.load_members("librarian")
                self.refresh_dashboard_stats()
            else:
                view.show_error(
                    "Error",
                    "Failed to delete librarian account."
                )

    # OLD METHOD NAMES KEPT FOR COMPATIBILITY
    def edit_librarian(self):
        self.update_selected_account()

    def delete_librarian(self):
        self.delete_selected_account()

    def update_selected_user_status(self):
        self.update_selected_account()

    def back_to_admin_dashboard_from_members(self):
        if self.manage_members_view:
            self.manage_members_view.close()
            self.manage_members_view = None

        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    # ================= ADMIN INVENTORY =================

    def open_admin_inventory(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.admin_inventory_view = AdminInventoryView(self)
        self.admin_inventory_view.show()
        self.load_admin_inventory()

    def load_admin_inventory(self):
        books = BookModel.get_all_books()

        if self.admin_inventory_view:
            self.admin_inventory_view.populate_table(books)

    def filter_admin_inventory(self):
        if not self.admin_inventory_view:
            return

        selected_filter = self.admin_inventory_view.filter_combo.currentText().strip()

        if selected_filter == "All":
            books = BookModel.get_all_books()
        else:
            books = BookModel.get_books_by_status(selected_filter)

        self.admin_inventory_view.populate_table(books)

    def search_admin_inventory(self):
        if not self.admin_inventory_view:
            return

        keyword = self.admin_inventory_view.search_input.text().strip()

        if not keyword:
            self.filter_admin_inventory()
            return

        books = BookModel.search_books(keyword)

        selected_filter = self.admin_inventory_view.filter_combo.currentText().strip()

        if selected_filter != "All":
            books = [
                book for book in books
                if book["status"] == selected_filter
            ]

        self.admin_inventory_view.populate_table(books)

    def back_to_admin_dashboard_from_inventory(self):
        if self.admin_inventory_view:
            self.admin_inventory_view.close()
            self.admin_inventory_view = None

        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    # ================= REPORTS =================

    def open_reports(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.reports_view = ReportsView(self)
        self.reports_view.show()
        self.generate_admin_report()

    def open_reports_view(self):
        self.open_reports()

    def _get_generated_by(self):
        user = self.auth_controller.current_user

        if not user:
            return "Unknown"

        role = user["role"].capitalize()
        return f"{user['first_name']} {user['last_name']} ({role})"

    def _filter_report_records(self):
        records = BorrowModel.get_all_borrow_records()

        if not self.reports_view:
            return records

        start_date, end_date = self.reports_view.get_date_range()
        filtered_records = []

        for record in records:
            borrow_date = record.get("borrow_date")
            return_date = record.get("return_date")

            if hasattr(borrow_date, "date"):
                borrow_date = borrow_date.date()

            if hasattr(return_date, "date"):
                return_date = return_date.date()

            include_record = False

            if borrow_date and start_date <= borrow_date <= end_date:
                include_record = True

            if return_date and start_date <= return_date <= end_date:
                include_record = True

            if include_record:
                filtered_records.append(record)

        return filtered_records

    def _get_book_copy_totals(self):
        books = BookModel.get_all_books()

        total_copies = 0
        available_copies = 0
        borrowed_copies = 0
        lost_copies = 0

        for book in books:
            total_copies += int(book.get("total_copies", 0) or 0)
            available_copies += int(book.get("available_copies", 0) or 0)
            borrowed_copies += int(book.get("borrowed_copies", 0) or 0)
            lost_copies += int(book.get("lost_copies", 0) or 0)

        return {
            "books": books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "borrowed_copies": borrowed_copies,
            "lost_copies": lost_copies
        }

    def generate_admin_report(self):
        if not self.reports_view:
            return

        records = self._filter_report_records()
        today = date.today()
        start_date, end_date = self.reports_view.get_date_range()

        copy_totals = self._get_book_copy_totals()

        total_records = len(records)

        total_returned = len([
            r for r in records
            if r["status"] == "Returned"
        ])

        overdue_records = []

        for record in records:
            due_date = record["due_date"]

            if hasattr(due_date, "date"):
                due_date = due_date.date()

            if record["status"] == "Borrowed" and due_date < today:
                overdue_records.append(record)

        total_overdue = len(overdue_records)

        total_penalty = sum(
            float(r["penalty"]) if r["penalty"] else 0
            for r in records
        )

        total_condition_fee = sum(
            float(r.get("condition_fee", 0)) if r.get("condition_fee") else 0
            for r in records
        )

        total_users = UserModel.count_users_by_role("student")
        total_librarians = UserModel.count_users_by_role("librarian")

        # Kept for compatibility. In your latest ReportsView, set_stats() is pass.
        self.reports_view.set_stats(
            total_records,
            total_returned,
            total_overdue,
            total_penalty
        )

        visual_data = {
            "requested_by": self._get_generated_by(),
            "generated_on": datetime.now().strftime("%B %d, %Y %I:%M %p"),
            "date_range": f"{start_date} to {end_date}",

            "total_books": copy_totals["total_copies"],
            "available_books": copy_totals["available_copies"],
            "borrowed_books": copy_totals["borrowed_copies"],
            "lost_books": copy_totals["lost_copies"],

            "total_users": total_users,
            "total_librarians": total_librarians,

            "total_transactions": total_records,
            "total_returned": total_returned,
            "total_overdue": total_overdue,
            "total_penalty": total_penalty,
            "total_condition_fee": total_condition_fee,

            "recent_transactions": records[:5]
        }

        if hasattr(self.reports_view, "set_visual_report"):
            self.reports_view.set_visual_report(visual_data)

    def export_admin_report_pdf(self):
        if not self.reports_view:
            return

        records = self._filter_report_records()
        today = date.today()
        start_date, end_date = self.reports_view.get_date_range()

        members = UserModel.get_users_by_role("student")
        librarians = UserModel.get_users_by_role("librarian")

        copy_totals = self._get_book_copy_totals()
        books = copy_totals["books"]

        total_transactions = len(records)

        total_returned = len([
            r for r in records
            if r["status"] == "Returned"
        ])

        overdue_records = []

        for record in records:
            due_date = record["due_date"]

            if hasattr(due_date, "date"):
                due_date = due_date.date()

            if record["status"] == "Borrowed" and due_date < today:
                overdue_records.append(record)

        total_overdue = len(overdue_records)

        total_penalty = sum(
            float(r["penalty"]) if r["penalty"] else 0
            for r in records
        )

        total_condition_fee = sum(
            float(r.get("condition_fee", 0)) if r.get("condition_fee") else 0
            for r in records
        )

        total_books = copy_totals["total_copies"]
        available_books = copy_totals["available_copies"]
        borrowed_books = copy_totals["borrowed_copies"]
        lost_books = copy_totals["lost_copies"]

        total_members = len(members)
        total_librarians = len(librarians)

        recent_transactions = records[:10]

        file_path, _ = QFileDialog.getSaveFileName(
            self.reports_view,
            "Save PDF Report",
            "BookWise_Full_Report.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        def transaction_rows(items):
            if not items:
                return """
                <tr>
                    <td colspan="11" style="text-align:center; color:#777;">
                        No transaction records found.
                    </td>
                </tr>
                """

            html = ""

            for record in items:
                penalty = float(record["penalty"]) if record["penalty"] else 0
                condition_fee = float(record.get("condition_fee", 0)) if record.get("condition_fee") else 0
                late_days = int(record.get("late_days", 0) or 0)
                condition = record.get("book_condition", "Good")

                html += f"""
                <tr>
                    <td>{record['id']}</td>
                    <td>{record['student_name']}</td>
                    <td>{record['book_title']}</td>
                    <td>{record['borrow_date']}</td>
                    <td>{record['due_date']}</td>
                    <td>{record['return_date'] or '-'}</td>
                    <td>{late_days}</td>
                    <td>{condition}</td>
                    <td>₱{condition_fee:.2f}</td>
                    <td>₱{penalty:.2f}</td>
                    <td>{record['status']}</td>
                </tr>
                """

            return html

        def member_rows(items, role_name):
            if not items:
                return f"""
                <tr>
                    <td colspan="5" style="text-align:center; color:#777;">
                        No {role_name} records found.
                    </td>
                </tr>
                """

            html = ""

            for user in items:
                full_name = f"{user['first_name']} {user['last_name']}"

                html += f"""
                <tr>
                    <td>{user['id']}</td>
                    <td>{full_name}</td>
                    <td>{user['email']}</td>
                    <td>{role_name}</td>
                    <td>{user.get('status', 'Active')}</td>
                </tr>
                """

            return html

        def book_rows(items):
            if not items:
                return """
                <tr>
                    <td colspan="9" style="text-align:center; color:#777;">
                        No book records found.
                    </td>
                </tr>
                """

            html = ""

            for book in items:
                html += f"""
                <tr>
                    <td>{book['id']}</td>
                    <td>{book['title']}</td>
                    <td>{book['author']}</td>
                    <td>{book['category'] or '-'}</td>
                    <td>{book.get('total_copies', 0)}</td>
                    <td>{book.get('available_copies', 0)}</td>
                    <td>{book.get('borrowed_copies', 0)}</td>
                    <td>{book.get('lost_copies', 0)}</td>
                    <td>{book['status']}</td>
                </tr>
                """

            return html

        html = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Arial;
                color: #1f2937;
                margin: 28px;
            }}

            h1 {{
                font-size: 24px;
                margin-bottom: 4px;
                color: #111827;
            }}

            .subtitle {{
                font-size: 12px;
                color: #6b7280;
                margin-bottom: 18px;
            }}

            .meta {{
                border: 1px solid #e5e7eb;
                background: #f9fafb;
                padding: 12px;
                border-radius: 10px;
                font-size: 11px;
                margin-bottom: 18px;
            }}

            .section-title {{
                font-size: 15px;
                font-weight: bold;
                margin-top: 22px;
                margin-bottom: 8px;
                color: #111827;
            }}

            .stats-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 14px;
            }}

            .stats-table td {{
                width: 25%;
                border: 1px solid #e5e7eb;
                background: #f9fafb;
                padding: 10px;
                font-size: 11px;
            }}

            .stat-number {{
                font-size: 18px;
                font-weight: bold;
                color: #111827;
            }}

            .stat-label {{
                font-size: 10px;
                color: #6b7280;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 12px;
            }}

            th {{
                background: #111827;
                color: white;
                padding: 6px;
                font-size: 9px;
                text-align: left;
            }}

            td {{
                padding: 6px;
                border-bottom: 1px solid #e5e7eb;
                font-size: 9px;
            }}

            .footer {{
                margin-top: 24px;
                font-size: 10px;
                color: #6b7280;
                text-align: center;
            }}
        </style>
        </head>

        <body>
            <h1>BookWise Library Management System</h1>
            <div class="subtitle">Complete Library Administrative Report</div>

            <div class="meta">
                <b>Requested By:</b> {self._get_generated_by()}<br>
                <b>Generated On:</b> {datetime.now().strftime("%B %d, %Y %I:%M %p")}<br>
                <b>Date Range:</b> {start_date} to {end_date}
            </div>

            <div class="section-title">Library Statistics</div>

            <table class="stats-table">
                <tr>
                    <td>
                        <div class="stat-number">{total_books}</div>
                        <div class="stat-label">Total Copies</div>
                    </td>
                    <td>
                        <div class="stat-number">{available_books}</div>
                        <div class="stat-label">Available Copies</div>
                    </td>
                    <td>
                        <div class="stat-number">{borrowed_books}</div>
                        <div class="stat-label">Borrowed Copies</div>
                    </td>
                    <td>
                        <div class="stat-number">{lost_books}</div>
                        <div class="stat-label">Lost Copies</div>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="stat-number">{total_transactions}</div>
                        <div class="stat-label">Transactions</div>
                    </td>
                    <td>
                        <div class="stat-number">{total_returned}</div>
                        <div class="stat-label">Returned</div>
                    </td>
                    <td>
                        <div class="stat-number">{total_overdue}</div>
                        <div class="stat-label">Overdue</div>
                    </td>
                    <td>
                        <div class="stat-number">₱{total_penalty:.2f}</div>
                        <div class="stat-label">Total Penalty</div>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="stat-number">{total_members}</div>
                        <div class="stat-label">Users</div>
                    </td>
                    <td>
                        <div class="stat-number">{total_librarians}</div>
                        <div class="stat-label">Librarians</div>
                    </td>
                    <td>
                        <div class="stat-number">₱{total_condition_fee:.2f}</div>
                        <div class="stat-label">Condition Fees</div>
                    </td>
                    <td>
                        <div class="stat-number">{len(books)}</div>
                        <div class="stat-label">Book Titles</div>
                    </td>
                </tr>
            </table>

            <div class="section-title">Recent Transactions</div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Book</th>
                    <th>Borrow Date</th>
                    <th>Due Date</th>
                    <th>Return Date</th>
                    <th>Late Days</th>
                    <th>Condition</th>
                    <th>Condition Fee</th>
                    <th>Total Penalty</th>
                    <th>Status</th>
                </tr>
                {transaction_rows(recent_transactions)}
            </table>

            <div class="section-title">Member Report - Users</div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                </tr>
                {member_rows(members, "User")}
            </table>

            <div class="section-title">Member Report - Librarians</div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                </tr>
                {member_rows(librarians, "Librarian")}
            </table>

            <div class="section-title">Book Inventory Report</div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Category</th>
                    <th>Total</th>
                    <th>Available</th>
                    <th>Borrowed</th>
                    <th>Lost</th>
                    <th>Status</th>
                </tr>
                {book_rows(books)}
            </table>

            <div class="footer">
                This report was generated by BookWise Library Management System.
            </div>
        </body>
        </html>
        """

        document = QTextDocument()
        document.setHtml(html)

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)

        document.print(printer)

        QMessageBox.information(
            self.reports_view,
            "Success",
            "Full PDF report generated successfully."
        )

    def back_to_admin_dashboard_from_reports(self):
        if self.reports_view:
            self.reports_view.close()
            self.reports_view = None

        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    # ================= CLEANUP =================

    def close_all_views(self):
        if self.manage_members_view:
            self.manage_members_view.close()
            self.manage_members_view = None

        if self.reports_view:
            self.reports_view.close()
            self.reports_view = None

        if self.admin_inventory_view:
            self.admin_inventory_view.close()
            self.admin_inventory_view = None

        if self.create_librarian_popup:
            self.create_librarian_popup.close()
            self.create_librarian_popup = None