from datetime import datetime

from models.user_model import UserModel
from models.book_model import BookModel
from models.borrow_model import BorrowModel

from views.borrow_return_view import BorrowReturnView
from views.borrow_receipt_view import BorrowReceiptView
from views.return_book_view import ReturnBookView


class BorrowController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.librarian_dashboard = None
        self.borrow_return_view = None
        self.borrow_receipt_view = None
        self.return_book_view = None
        self.current_return_record = None

    def set_librarian_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard

    # ================= OPEN BORROW / RETURN =================

    def open_borrow_return(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.borrow_return_view = BorrowReturnView(self)
        self.borrow_return_view.show()
        self.load_borrow_return_data()

    def load_borrow_return_data(self):
        records = BorrowModel.get_all_borrow_records()

        if self.borrow_return_view:
            self.borrow_return_view.populate_table(records)

    # ================= BORROW LOOKUP =================

    def lookup_borrow_fields(self):
        if not self.borrow_return_view:
            return

        user_text = "User: -"
        book_text = "Book: -"

        user_id_text = self.borrow_return_view.user_id_input.text().strip()
        book_id_text = self.borrow_return_view.book_id_input.text().strip()

        if user_id_text.isdigit():
            user = UserModel.get_user_by_id(int(user_id_text))

            if not user:
                user_text = "User: Not found"
            elif user["role"] != "student":
                user_text = "User: Invalid user role"
            elif user.get("status", "Active") != "Active":
                user_text = f"User: {user['first_name']} {user['last_name']} (Inactive)"
            else:
                user_text = f"User: {user['first_name']} {user['last_name']}"

        if book_id_text.isdigit():
            book = BookModel.get_book_by_id(int(book_id_text))

            if not book:
                book_text = "Book: Not found"
            else:
                available_copies = int(book.get("available_copies", 0) or 0)

                if available_copies <= 0:
                    book_text = f"Book: {book['title']} (No available copies)"
                else:
                    book_text = f"Book: {book['title']} ({available_copies} available)"

        self.borrow_return_view.set_lookup_labels(user_text, book_text)

    # ================= BORROW ACTION =================

    def borrow_book_by_id(self):
        if not self.borrow_return_view:
            return

        user_id_text = self.borrow_return_view.user_id_input.text().strip()
        book_id_text = self.borrow_return_view.book_id_input.text().strip()

        if not user_id_text.isdigit() or not book_id_text.isdigit():
            self.borrow_return_view.show_error(
                "Error",
                "Please enter valid numeric User ID and Book ID."
            )
            return

        member_id = int(user_id_text)
        book_id = int(book_id_text)

        user = UserModel.get_user_by_id(member_id)

        if not user:
            self.borrow_return_view.show_error("Error", "User ID not found.")
            return

        if user["role"] != "student":
            self.borrow_return_view.show_error("Error", "Only users can borrow books.")
            return

        if user.get("status", "Active") != "Active":
            self.borrow_return_view.show_error("Error", "This user account is inactive.")
            return

        book = BookModel.get_book_by_id(book_id)

        if not book:
            self.borrow_return_view.show_error("Error", "Book ID not found.")
            return

        available_copies = int(book.get("available_copies", 0) or 0)

        if available_copies <= 0:
            self.borrow_return_view.show_error(
                "Error",
                "This book has no available copies."
            )
            return

        result = BorrowModel.create_borrow(member_id, book_id)

        if not result:
            self.borrow_return_view.show_error("Error", "Failed to create borrow record.")
            return

        copy_success = BookModel.borrow_one_copy(book_id)

        if not copy_success:
            self.borrow_return_view.show_error(
                "Error",
                "Failed to update book copies."
            )
            return

        student_name = f"{user['first_name']} {user['last_name']}"
        transaction_date = datetime.now().strftime("%B %d, %Y - %I:%M %p")

        current_user = self.auth_controller.current_user
        librarian_name = "Unknown"

        if current_user:
            librarian_name = f"{current_user['first_name']} {current_user['last_name']}"

        updated_book = BookModel.get_book_by_id(book_id)

        receipt_data = {
            "receipt_no": f"BR-{result['record_id']:05d}",
            "transaction_date": transaction_date,
            "member_id": member_id,
            "student_name": student_name,
            "book_id": book_id,
            "book_title": book["title"],
            "borrow_date": str(result["borrow_date"]),
            "due_date": str(result["due_date"]),
            "status": result["status"],
            "librarian_name": librarian_name
        }

        self.borrow_receipt_view = BorrowReceiptView(receipt_data)
        self.borrow_receipt_view.show()

        remaining = updated_book.get("available_copies", 0) if updated_book else 0

        self.borrow_return_view.show_message(
            "Success",
            f"Book borrowed successfully.\n\nAvailable copies left: {remaining}"
        )

        self.borrow_return_view.clear_borrow_inputs()
        self.load_borrow_return_data()
        self.refresh_librarian_dashboard()

    # ================= RETURN WINDOW =================

    def open_return_window(self):
        self.current_return_record = None
        self.return_book_view = ReturnBookView(self)
        self.return_book_view.show()

    def lookup_return_book(self):
        if not self.return_book_view:
            return

        book_id_text = self.return_book_view.book_id_input.text().strip()
        self.current_return_record = None

        if not book_id_text:
            self.return_book_view.set_details_text(
                "Borrowed record details will appear here."
            )
            return

        if not book_id_text.isdigit():
            self.return_book_view.set_details_text(
                "Please enter a valid numeric Book ID."
            )
            return

        book_id = int(book_id_text)
        record = BorrowModel.get_active_borrow_by_book_id(book_id)

        if not record:
            self.return_book_view.set_details_text(
                "No active borrowed record found for this Book ID."
            )
            return

        self.current_return_record = record

        details = (
            f"Record ID: {record['id']}\n"
            f"User: {record['student_name']}\n"
            f"Book: {record['book_title']}\n"
            f"Borrow Date: {record['borrow_date']}\n"
            f"Due Date: {record['due_date']}\n"
            f"Status: {record['status']}\n\n"
            f"Choose condition before returning:\n"
            f"Good = normal return\n"
            f"Damaged = add ₱100 fee\n"
            f"Lost = add ₱500 fee and reduce available copies"
        )

        self.return_book_view.set_details_text(details)

    def return_book_by_book_id(self):
        if not self.return_book_view:
            return

        if not self.current_return_record:
            self.return_book_view.show_error(
                "Error",
                "No active borrowed record found for this Book ID."
            )
            return

        record_id = self.current_return_record["id"]
        book_id = self.current_return_record["book_id"]
        condition = self.return_book_view.get_condition()

        result = BorrowModel.return_book(record_id, condition)

        if not result:
            self.return_book_view.show_error("Error", "Failed to return book.")
            return

        copy_success = BookModel.return_one_copy(book_id, condition)

        if not copy_success:
            self.return_book_view.show_error(
                "Error",
                "Return record saved, but failed to update book copies."
            )
            return

        updated_book = BookModel.get_book_by_id(book_id)

        late_days = result.get("late_days", 0)
        overdue_penalty = result.get("overdue_penalty", 0)
        condition_fee = result.get("condition_fee", 0)
        total_penalty = result.get("penalty", 0)
        available = updated_book.get("available_copies", 0) if updated_book else 0
        lost = updated_book.get("lost_copies", 0) if updated_book else 0

        self.return_book_view.show_message(
            "Returned",
            f"Book return processed successfully.\n\n"
            f"Condition: {condition}\n"
            f"Late Days: {late_days}\n"
            f"Overdue Penalty: ₱{overdue_penalty:.2f}\n"
            f"Condition Fee: ₱{condition_fee:.2f}\n"
            f"Total Penalty: ₱{total_penalty:.2f}\n\n"
            f"Available Copies: {available}\n"
            f"Lost Copies: {lost}"
        )

        self.return_book_view.clear_input()
        self.current_return_record = None
        self.load_borrow_return_data()
        self.refresh_librarian_dashboard()

    # ================= DASHBOARD / CLOSE =================

    def refresh_librarian_dashboard(self):
        if self.auth_controller and hasattr(self.auth_controller, "librarian_controller"):
            self.auth_controller.librarian_controller.refresh_dashboard_stats()

        if self.auth_controller and hasattr(self.auth_controller, "admin_controller"):
            self.auth_controller.admin_controller.refresh_dashboard_stats()

    def back_to_librarian_dashboard_from_borrow_return(self):
        if self.borrow_return_view:
            self.borrow_return_view.close()
            self.borrow_return_view = None

        if self.librarian_dashboard:
            self.refresh_librarian_dashboard()
            self.librarian_dashboard.show()

    def close_all_views(self):
        if self.borrow_return_view:
            self.borrow_return_view.close()
            self.borrow_return_view = None

        if self.borrow_receipt_view:
            self.borrow_receipt_view.close()
            self.borrow_receipt_view = None

        if self.return_book_view:
            self.return_book_view.close()
            self.return_book_view = None

        self.current_return_record = None