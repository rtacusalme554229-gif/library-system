from models.book_model import BookModel
from views.manage_books_view import ManageBooksView


class BookController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.manage_books_view = None

        # Compatibility references
        self.librarian_dashboard = None
        self.admin_dashboard = None
        self.student_dashboard = None

    # ================= COMPATIBILITY METHODS =================

    def set_librarian_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard

    def set_admin_dashboard(self, dashboard):
        self.admin_dashboard = dashboard

    def set_student_dashboard(self, dashboard):
        self.student_dashboard = dashboard

    # ================= OPEN MANAGE BOOKS =================

    def open_manage_books(self):
        librarian_controller = getattr(self.auth_controller, "librarian_controller", None)

        if librarian_controller and librarian_controller.librarian_dashboard:
            librarian_controller.librarian_dashboard.hide()
        elif self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.manage_books_view = ManageBooksView(self)
        self.manage_books_view.show()
        self.load_books()

    # ================= LOAD / SEARCH / FILTER =================

    def load_books(self):
        books = BookModel.get_all_books()

        if self.manage_books_view:
            self.manage_books_view.populate_table(books)

    def search_books(self):
        if not self.manage_books_view:
            return

        keyword = self.manage_books_view.search_input.text().strip()
        selected_filter = self.manage_books_view.filter_combo.currentText()

        if keyword:
            books = BookModel.search_books(keyword)
        else:
            books = BookModel.get_all_books()

        if selected_filter != "All":
            books = [
                book for book in books
                if book["status"] == selected_filter
            ]

        self.manage_books_view.populate_table(books)

    def filter_books(self):
        self.search_books()

    # ================= ADD BOOK =================

    def add_book(self):
        if not self.manage_books_view:
            return

        data = self.manage_books_view.get_form_data()

        title = data["title"]
        author = data["author"]
        category = data["category"]
        total_copies = data["total_copies"]

        if not all([title, author, category, total_copies]):
            self.manage_books_view.show_error(
                "Error",
                "Please fill in all book details."
            )
            return

        try:
            total_copies = int(total_copies)
        except ValueError:
            self.manage_books_view.show_error(
                "Error",
                "Total copies must be a number."
            )
            return

        if total_copies < 1:
            self.manage_books_view.show_error(
                "Error",
                "Total copies must be at least 1."
            )
            return

        book_id = BookModel.add_book(
            title,
            author,
            category,
            total_copies
        )

        if book_id:
            self.manage_books_view.show_message(
                "Success",
                "Book added successfully."
            )
            self.manage_books_view.clear_form()
            self.load_books()
            self.refresh_librarian_dashboard()
        else:
            self.manage_books_view.show_error(
                "Error",
                "Failed to add book."
            )

    # ================= UPDATE BOOK =================

    def update_book(self):
        if not self.manage_books_view:
            return

        if not self.manage_books_view.selected_book_id:
            self.manage_books_view.show_error(
                "Error",
                "Please select a book first."
            )
            return

        data = self.manage_books_view.get_form_data()

        title = data["title"]
        author = data["author"]
        category = data["category"]
        total_copies = data["total_copies"]

        if not all([title, author, category, total_copies]):
            self.manage_books_view.show_error(
                "Error",
                "Please fill in all book details."
            )
            return

        try:
            total_copies = int(total_copies)
        except ValueError:
            self.manage_books_view.show_error(
                "Error",
                "Total copies must be a number."
            )
            return

        success = BookModel.update_book(
            self.manage_books_view.selected_book_id,
            title,
            author,
            category,
            total_copies
        )

        if success:
            self.manage_books_view.show_message(
                "Success",
                "Book information updated successfully."
            )
            self.manage_books_view.clear_form()
            self.load_books()
            self.refresh_librarian_dashboard()
        else:
            self.manage_books_view.show_error(
                "Error",
                "Failed to update book. Total copies cannot be less than borrowed + lost copies."
            )

    # ================= DELETE BOOK =================

    def delete_book(self):
        if not self.manage_books_view:
            return

        if not self.manage_books_view.selected_book_id:
            self.manage_books_view.show_error(
                "Error",
                "Please select a book first."
            )
            return

        success = BookModel.delete_book(self.manage_books_view.selected_book_id)

        if success:
            self.manage_books_view.show_message(
                "Success",
                "Book deleted successfully."
            )
            self.manage_books_view.clear_form()
            self.load_books()
            self.refresh_librarian_dashboard()
        else:
            self.manage_books_view.show_error(
                "Error",
                "Failed to delete book. Book may still have borrowed copies."
            )

    # ================= REFRESH DASHBOARDS =================

    def refresh_librarian_dashboard(self):
        librarian_controller = getattr(self.auth_controller, "librarian_controller", None)

        if librarian_controller:
            librarian_controller.refresh_dashboard_stats()

    def refresh_admin_dashboard(self):
        admin_controller = getattr(self.auth_controller, "admin_controller", None)

        if admin_controller:
            admin_controller.refresh_dashboard_stats()

    # ================= BACK =================

    def back_to_librarian_dashboard_from_books(self):
        if self.manage_books_view:
            self.manage_books_view.close()
            self.manage_books_view = None

        librarian_controller = getattr(self.auth_controller, "librarian_controller", None)

        if librarian_controller and librarian_controller.librarian_dashboard:
            librarian_controller.refresh_dashboard_stats()
            librarian_controller.librarian_dashboard.show()
        elif self.librarian_dashboard:
            self.librarian_dashboard.show()

    # ================= CLOSE =================

    def close_all_views(self):
        if self.manage_books_view:
            self.manage_books_view.close()
            self.manage_books_view = None