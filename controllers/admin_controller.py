from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter

from datetime import datetime, date

from models.user_model import UserModel
from models.book_model import BookModel
from models.borrow_model import BorrowModel
from views.create_librarian_view import CreateLibrarianView
from views.manage_members_view import ManageMembersView
from views.reports_view import ReportsView
from views.admin_inventory_view import AdminInventoryView


class AdminController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.admin_dashboard = None
        self.create_librarian_view = None
        self.manage_members_view = None
        self.reports_view = None
        self.admin_inventory_view = None

    def set_dashboard(self, dashboard):
        self.admin_dashboard = dashboard
        self.refresh_dashboard_stats()

    def refresh_dashboard_stats(self):
        if not self.admin_dashboard:
            return

        total_books = BookModel.count_all_books()
        available_books = BookModel.count_available_books()
        borrowed_books = BookModel.count_borrowed_books()
        total_students = UserModel.count_users_by_role("student")
        total_librarians = UserModel.count_users_by_role("librarian")
        total_members = total_students + total_librarians

        self.admin_dashboard.set_stats(
            total_books,
            available_books,
            borrowed_books,
            total_members
        )

    def logout(self):
        self.auth_controller.logout()

    # ================= CREATE LIBRARIAN =================

    def open_create_librarian(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.create_librarian_view = CreateLibrarianView(self)
        self.create_librarian_view.show()

    def back_to_admin_dashboard(self):
        if self.create_librarian_view:
            self.create_librarian_view.close()
        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    def save_librarian(self):
        first_name = self.create_librarian_view.first_name_input.text().strip()
        last_name = self.create_librarian_view.last_name_input.text().strip()
        email = self.create_librarian_view.email_input.text().strip()
        address = self.create_librarian_view.address_input.text().strip()
        password = self.create_librarian_view.password_input.text().strip()

        if not all([first_name, last_name, email, address, password]):
            self.create_librarian_view.show_error("Error", "Please fill in all fields.")
            return

        existing_user = UserModel.find_by_email(email)
        if existing_user:
            self.create_librarian_view.show_error("Error", "Email already exists.")
            return

        librarian_id = UserModel.create_librarian(
            first_name, last_name, email, address, password
        )

        if librarian_id:
            self.create_librarian_view.show_message("Success", "Librarian account created successfully.")
            self.create_librarian_view.close()
            if self.admin_dashboard:
                self.refresh_dashboard_stats()
                self.admin_dashboard.show()
        else:
            self.create_librarian_view.show_error("Error", "Failed to create librarian account.")

    # ================= MANAGE MEMBERS =================

    def open_manage_members(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.manage_members_view = ManageMembersView(self)
        self.manage_members_view.show()
        self.load_members("librarian")

    def load_members(self, role):
        users = UserModel.get_users_by_role(role)
        if self.manage_members_view:
            self.manage_members_view.populate_table(users, role)

    def edit_librarian(self):
        view = self.manage_members_view

        if not view:
            return

        if view.current_role != "librarian":
            view.show_error("Error", "You can only update librarians in this section.")
            return

        if not view.selected_user_id:
            view.show_error("Error", "Please select a librarian first.")
            return

        first_name = view.first_name_input.text().strip()
        last_name = view.last_name_input.text().strip()
        email = view.email_input.text().strip()
        address = view.address_input.text().strip()

        if not all([first_name, last_name, email, address]):
            view.show_error("Error", "Please fill in all librarian fields.")
            return

        existing_user = UserModel.find_by_email(email)
        if existing_user and existing_user["id"] != view.selected_user_id:
            view.show_error("Error", "Email already exists.")
            return

        success = UserModel.update_librarian(
            view.selected_user_id,
            first_name,
            last_name,
            email,
            address
        )

        if success:
            view.show_message("Success", "Librarian updated successfully.")
            self.load_members("librarian")
            self.refresh_dashboard_stats()
        else:
            view.show_error("Error", "Failed to update librarian.")

    def delete_librarian(self):
        view = self.manage_members_view

        if not view:
            return

        if view.current_role != "librarian":
            view.show_error("Error", "You can only delete librarians in this section.")
            return

        if not view.selected_user_id:
            view.show_error("Error", "Please select a librarian first.")
            return

        reply = QMessageBox.question(
            view,
            "Confirm Delete",
            "Are you sure you want to delete this librarian?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = UserModel.delete_librarian(view.selected_user_id)

            if success:
                view.show_message("Success", "Librarian deleted successfully.")
                self.load_members("librarian")
                self.refresh_dashboard_stats()
            else:
                view.show_error("Error", "Failed to delete librarian.")

    def back_to_admin_dashboard_from_members(self):
        if self.manage_members_view:
            self.manage_members_view.close()
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
        elif selected_filter == "Available":
            books = BookModel.get_books_by_status("Available")
        elif selected_filter == "Borrowed":
            books = BookModel.get_books_by_status("Borrowed")
        else:
            books = BookModel.get_all_books()

        self.admin_inventory_view.populate_table(books)

    def search_admin_inventory(self):
        if not self.admin_inventory_view:
            return

        keyword = self.admin_inventory_view.search_input.text().strip()

        if not keyword:
            self.filter_admin_inventory()
            return

        books = BookModel.search_books(keyword)
        self.admin_inventory_view.populate_table(books)

    def back_to_admin_dashboard_from_inventory(self):
        if self.admin_inventory_view:
            self.admin_inventory_view.close()
        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    # ================= REPORT HELPERS =================

    def _build_user_borrow_stats(self):
        users = UserModel.get_all_users()
        records = BorrowModel.get_all_borrow_records()

        today = date.today()

        librarians = []
        students = []
        student_stats = {}

        for user in users:
            if user["role"] == "student":
                student_stats[user["id"]] = {
                    "id": user["id"],
                    "name": f"{user['first_name']} {user['last_name']}",
                    "role": "Student",
                    "borrowed": 0,
                    "overdue": 0,
                    "status": "Active"
                }

            elif user["role"] == "librarian":
                librarians.append({
                    "id": user["id"],
                    "name": f"{user['first_name']} {user['last_name']}",
                    "role": "Librarian",
                    "status": "Active"
                })

        for record in records:
            member_id = record.get("member_id")

            if member_id in student_stats:
                if record["status"] == "Borrowed":
                    student_stats[member_id]["borrowed"] += 1

                    due_date = record.get("due_date")
                    if due_date:
                        try:
                            if hasattr(due_date, "year"):
                                due_as_date = due_date
                            else:
                                due_as_date = datetime.strptime(str(due_date), "%Y-%m-%d").date()

                            if due_as_date < today:
                                student_stats[member_id]["overdue"] += 1
                        except Exception:
                            pass

        students = list(student_stats.values())
        return librarians, students

    # ================= REPORTS =================

    def open_reports(self):
        if self.admin_dashboard:
            self.admin_dashboard.hide()

        self.reports_view = ReportsView(self)
        self.reports_view.show()

        total_books = BookModel.count_all_books()
        total_students = UserModel.count_users_by_role("student")
        total_librarians = UserModel.count_users_by_role("librarian")
        total_members = total_students + total_librarians

        self.reports_view.set_stats(total_books, total_members)
        self.generate_admin_report()

    def generate_admin_report(self):
        if not self.reports_view:
            return

        total_books = BookModel.count_all_books()
        available_books = BookModel.count_available_books()
        borrowed_books = BookModel.count_borrowed_books()
        total_students = UserModel.count_users_by_role("student")
        total_librarians = UserModel.count_users_by_role("librarian")
        total_members = total_students + total_librarians

        records = BorrowModel.get_all_borrow_records()
        librarians, students = self._build_user_borrow_stats()

        total_penalty_collected = 0
        transaction_lines = []

        for record in records:
            penalty_value = float(record["penalty"]) if record["penalty"] else 0
            total_penalty_collected += penalty_value

            transaction_lines.append(
                f"{record['borrow_date']} | {record['student_name']} | "
                f"{record['book_title']} | {record['status']}"
            )

        if not transaction_lines:
            transaction_lines.append("No transactions available.")

        librarian_lines = []
        for librarian in librarians:
            librarian_lines.append(
                f"{librarian['name']} | ID:{librarian['id']} | {librarian['role']} | {librarian['status']}"
            )

        if not librarian_lines:
            librarian_lines.append("No librarians available.")

        student_lines = []
        for student in students:
            student_lines.append(
                f"{student['name']} | ID:{student['id']} | Borrowed:{student['borrowed']} | "
                f"Overdue:{student['overdue']} | {student['status']}"
            )

        if not student_lines:
            student_lines.append("No students available.")

        report_text = f"""
BOOKWISE LIBRARY MANAGEMENT SYSTEM
Complete Library Report
Generated: {datetime.now().strftime("%B %d, %Y %I:%M %p")}

==================== SUMMARY ====================

Total Books: {total_books}
Available Books: {available_books}
Borrowed Books: {borrowed_books}
Registered Members: {total_members}
Total Penalty Collected: ₱{total_penalty_collected:.2f}

==================== RECENT TRANSACTIONS ====================

""" + "\n".join(transaction_lines) + """

==================== LIBRARIAN REPORT ====================

""" + "\n".join(librarian_lines) + """

==================== USER REPORT ====================

""" + "\n".join(student_lines)

        self.reports_view.set_report_text(report_text)

    def export_admin_report_pdf(self):
        if not self.reports_view:
            return

        records = BorrowModel.get_all_borrow_records()
        books = BookModel.get_all_books()
        librarians, students = self._build_user_borrow_stats()

        total_books = len(books)
        available_books = len([b for b in books if b["status"] == "Available"])
        borrowed_books = len([b for b in books if b["status"] == "Borrowed"])
        total_members = len(librarians) + len(students)

        transactions_html = ""
        for record in records:
            status_color = "#f59e0b" if record["status"] == "Borrowed" else "#22c55e"

            transactions_html += f"""
            <tr>
                <td>{record['borrow_date']}</td>
                <td>{record['student_name']}</td>
                <td>{record['book_title']}</td>
                <td style="color:{status_color}; font-weight:bold;">{record['status']}</td>
            </tr>
            """

        if not transactions_html:
            transactions_html = "<tr><td colspan='4'>No transactions available</td></tr>"

        librarian_html = ""
        for librarian in librarians:
            librarian_html += f"""
            <tr>
                <td>{librarian['name']}</td>
                <td>{librarian['id']}</td>
                <td>{librarian['role']}</td>
                <td style="color:#22c55e;">{librarian['status']}</td>
            </tr>
            """

        if not librarian_html:
            librarian_html = "<tr><td colspan='4'>No librarians available</td></tr>"

        student_html = ""
        for student in students:
            student_html += f"""
            <tr>
                <td>{student['name']}</td>
                <td>{student['id']}</td>
                <td>{student['role']}</td>
                <td>{student['borrowed']}</td>
                <td>{student['overdue']}</td>
                <td style="color:#22c55e;">{student['status']}</td>
            </tr>
            """

        if not student_html:
            student_html = "<tr><td colspan='6'>No students available</td></tr>"

        inventory_html = ""
        for book in books:
            status_color = "#22c55e" if book["status"] == "Available" else "#f59e0b"

            inventory_html += f"""
            <tr>
                <td>{book['title']}</td>
                <td>{book['author']}</td>
                <td>1</td>
                <td>1</td>
                <td>Main Library</td>
                <td style="color:{status_color}; font-weight:bold;">{book['status']}</td>
            </tr>
            """

        file_path, _ = QFileDialog.getSaveFileName(
            self.reports_view,
            "Save Report",
            "bookwise_clean_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        html = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Arial;
                margin: 30px;
                color: #1f2937;
            }}

            h1 {{
                font-size: 22px;
                margin-bottom: 5px;
            }}

            .section-title {{
                font-size: 16px;
                font-weight: bold;
                margin-top: 30px;
                margin-bottom: 10px;
            }}

            .stats {{
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
            }}

            .stat {{
                font-size: 28px;
                font-weight: bold;
            }}

            .blue {{ color:#3b82f6; }}
            .green {{ color:#22c55e; }}
            .orange {{ color:#f59e0b; }}
            .red {{ color:#ef4444; }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            th {{
                text-align: left;
                font-size: 12px;
                border-bottom: 2px solid #ddd;
                padding: 8px;
            }}

            td {{
                padding: 8px;
                border-bottom: 1px solid #eee;
                font-size: 11px;
            }}
        </style>
        </head>

        <body>

            <h1>📚 BookWise Library Management System</h1>
            <div style="font-size:12px; color:#6b7280;">
                Generated on: {datetime.now().strftime("%B %d, %Y")}
            </div>

            <div class="section-title">Library Statistics</div>

            <div class="stats">
                <div><div class="stat blue">{total_books}</div><div>Total Books</div></div>
                <div><div class="stat green">{available_books}</div><div>Available</div></div>
                <div><div class="stat orange">{borrowed_books}</div><div>Borrowed</div></div>
                <div><div class="stat red">{total_members}</div><div>Total Members</div></div>
            </div>

            <div class="section-title">Recent Transactions</div>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Member</th>
                    <th>Book</th>
                    <th>Status</th>
                </tr>
                {transactions_html}
            </table>

            <div class="section-title">Librarian Report</div>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Member ID</th>
                    <th>Role</th>
                    <th>Status</th>
                </tr>
                {librarian_html}
            </table>

            <div class="section-title">User Report</div>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Member ID</th>
                    <th>Role</th>
                    <th>Borrowed</th>
                    <th>Overdue</th>
                    <th>Status</th>
                </tr>
                {student_html}
            </table>

            <div class="section-title">Book Inventory Report</div>
            <table>
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Available</th>
                    <th>Total</th>
                    <th>Location</th>
                    <th>Status</th>
                </tr>
                {inventory_html}
            </table>

        </body>
        </html>
        """

        document = QTextDocument()
        document.setHtml(html)

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)

        document.print(printer)

        QMessageBox.information(self.reports_view, "Done", "Report exported successfully.")

    def back_to_admin_dashboard_from_reports(self):
        if self.reports_view:
            self.reports_view.close()
        if self.admin_dashboard:
            self.refresh_dashboard_stats()
            self.admin_dashboard.show()

    def close_all_views(self):
        if self.create_librarian_view:
            self.create_librarian_view.close()
        if self.manage_members_view:
            self.manage_members_view.close()
        if self.reports_view:
            self.reports_view.close()
        if self.admin_inventory_view:
            self.admin_inventory_view.close()