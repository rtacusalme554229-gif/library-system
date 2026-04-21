from datetime import datetime
from models.user_model import UserModel
from models.book_model import BookModel
from models.borrow_model import BorrowModel
from views.borrow_return_view import BorrowReturnView
from views.borrow_receipt_view import BorrowReceiptView


class BorrowController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.librarian_dashboard = None
        self.borrow_return_view = None
        self.borrow_receipt_view = None

    def set_librarian_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard

    def open_borrow_return(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.borrow_return_view = BorrowReturnView(self)
        self.borrow_return_view.show()
        self.load_borrow_return_data()

    def load_borrow_return_data(self):
        students = UserModel.get_students_with_contact()
        books = BookModel.get_available_books()
        records = BorrowModel.get_all_borrow_records()

        if self.borrow_return_view:
            self.borrow_return_view.load_student_combo(students)
            self.borrow_return_view.load_book_combo(books)
            self.borrow_return_view.populate_table(records)

    def borrow_book(self):
        member_id = self.borrow_return_view.student_combo.currentData()
        book_id = self.borrow_return_view.book_combo.currentData()

        if not member_id or not book_id:
            self.borrow_return_view.show_error("Error", "Please select both student and book.")
            return

        result = BorrowModel.create_borrow(member_id, book_id)

        if result:
            BookModel.set_book_status(book_id, "Borrowed")

            student_name = self.borrow_return_view.student_combo.currentText()
            book_title = self.borrow_return_view.book_combo.currentText()
            transaction_date = datetime.now().strftime("%B %d, %Y - %I:%M %p")

            current_user = self.auth_controller.current_user
            librarian_name = "Unknown Librarian"
            if current_user:
                librarian_name = f"{current_user['first_name']} {current_user['last_name']}"

            receipt_data = {
                "receipt_no": f"BR-{result['record_id']:05d}",
                "transaction_date": transaction_date,
                "member_id": member_id,
                "student_name": student_name,
                "book_id": book_id,
                "book_title": book_title,
                "borrow_date": str(result["borrow_date"]),
                "due_date": str(result["due_date"]),
                "status": result["status"],
                "librarian_name": librarian_name
            }

            self.borrow_receipt_view = BorrowReceiptView(receipt_data)
            self.borrow_receipt_view.show()

            self.borrow_return_view.show_message(
                "Success",
                "Book borrowed successfully.\nA receipt has been generated."
            )
            self.load_borrow_return_data()
        else:
            self.borrow_return_view.show_error("Error", "Failed to borrow book.")

    def return_selected_book(self):
        record_id = self.borrow_return_view.selected_record_id

        if not record_id:
            self.borrow_return_view.show_error("Error", "Please select a borrow record first.")
            return

        result = BorrowModel.return_book(record_id)

        if result:
            BookModel.set_book_status(result["book_id"], "Available")
            self.borrow_return_view.show_message(
                "Book Returned",
                f"Book returned successfully.\nPenalty: ₱{result['penalty']}"
            )
            self.load_borrow_return_data()
        else:
            self.borrow_return_view.show_error("Error", "Failed to return book or record already returned.")

    def back_to_librarian_dashboard_from_borrow_return(self):
        if self.borrow_return_view:
            self.borrow_return_view.close()
        if self.librarian_dashboard:
            self.librarian_dashboard.show()

    def close_all_views(self):
        if self.borrow_return_view:
            self.borrow_return_view.close()
        if self.borrow_receipt_view:
            self.borrow_receipt_view.close()