from models.borrow_model import BorrowModel
from models.book_model import BookModel


class StudentController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.dashboard = None

    def set_dashboard(self, dashboard):
        self.dashboard = dashboard
        self.load_dashboard_data()

    def load_dashboard_data(self):
        if not self.dashboard:
            return

        user = self.auth_controller.current_user
        if not user:
            return

        records = BorrowModel.get_borrow_records_by_student(user["id"])

        total = len(records)
        active = len([r for r in records if r["status"] == "Borrowed"])
        returned = len([r for r in records if r["status"] == "Returned"])

        self.dashboard.set_stats(total, active, returned)
        self.dashboard.populate_table(records)

        books = BookModel.get_books_by_status("Available")
        self.dashboard.populate_books_table(books)

    def search_books(self, keyword):
        if not self.dashboard:
            return

        try:
            if keyword:
                books = BookModel.search_books(keyword)
            else:
                books = BookModel.get_books_by_status("Available")

            books = [b for b in books if b["status"] == "Available"]
            self.dashboard.populate_books_table(books)

        except Exception as e:
            print("USER SEARCH ERROR:", e)

    def logout(self):
        self.auth_controller.logout()

    def close_all_views(self):
        if self.dashboard:
            self.dashboard.close()
            self.dashboard = None