from PyQt6.QtWidgets import QMessageBox
from models.book_model import BookModel
from views.manage_books_view import ManageBooksView
from views.search_books_view import SearchBooksView


class BookController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.librarian_dashboard = None
        self.student_dashboard = None
        self.manage_books_view = None
        self.search_books_view = None

    def set_librarian_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard

    def set_student_dashboard(self, dashboard):
        self.student_dashboard = dashboard

    def open_manage_books(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.manage_books_view = ManageBooksView(self)
        self.manage_books_view.show()
        self.load_books()

    def load_books(self):
        books = BookModel.get_all_books()
        if self.manage_books_view:
            self.manage_books_view.populate_table(books)

    def filter_books(self):
        if not self.manage_books_view:
            return

        selected_filter = self.manage_books_view.filter_combo.currentText()

        if selected_filter == "All":
            books = BookModel.get_all_books()
        else:
            books = BookModel.get_books_by_status(selected_filter)

        self.manage_books_view.populate_table(books)

    def save_book(self):
        title = self.manage_books_view.title_input.text().strip()
        author = self.manage_books_view.author_input.text().strip()
        category = self.manage_books_view.category_input.text().strip()
        status = self.manage_books_view.status_combo.currentText()

        if not all([title, author, category, status]):
            self.manage_books_view.show_error("Error", "Please fill in all fields.")
            return

        success = BookModel.create_book(title, author, category, status)

        if success:
            self.manage_books_view.show_message("Success", "Book added successfully.")
            self.manage_books_view.clear_form()
            self.filter_books()
        else:
            self.manage_books_view.show_error("Error", "Failed to add book.")

    def update_book(self):
        book_id = self.manage_books_view.selected_book_id
        title = self.manage_books_view.title_input.text().strip()
        author = self.manage_books_view.author_input.text().strip()
        category = self.manage_books_view.category_input.text().strip()
        status = self.manage_books_view.status_combo.currentText()

        if not book_id:
            self.manage_books_view.show_error("Error", "Please select a book first.")
            return

        if not all([title, author, category, status]):
            self.manage_books_view.show_error("Error", "Please fill in all fields.")
            return

        success = BookModel.update_book(book_id, title, author, category, status)

        if success:
            self.manage_books_view.show_message("Success", "Book updated successfully.")
            self.manage_books_view.clear_form()
            self.filter_books()
        else:
            self.manage_books_view.show_error("Error", "Failed to update book.")

    def delete_book(self):
        book_id = self.manage_books_view.selected_book_id

        if not book_id:
            self.manage_books_view.show_error("Error", "Please select a book first.")
            return

        reply = QMessageBox.question(
            self.manage_books_view,
            "Confirm Delete",
            "Are you sure you want to delete this book?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = BookModel.delete_book(book_id)

            if success:
                self.manage_books_view.show_message("Success", "Book deleted successfully.")
                self.manage_books_view.clear_form()
                self.filter_books()
            else:
                self.manage_books_view.show_error("Error", "Failed to delete book.")

    def back_to_librarian_dashboard_from_books(self):
        if self.manage_books_view:
            self.manage_books_view.close()
            self.manage_books_view = None
        if self.librarian_dashboard:
            self.librarian_dashboard.show()

    def open_search_books_librarian(self):
        self.auth_controller.search_books_source = "librarian"

        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.search_books_view = SearchBooksView(self)
        self.auth_controller.search_books_view = self.search_books_view
        self.search_books_view.show()
        self.load_all_books_for_search()

    def open_search_books_student(self):
        self.auth_controller.search_books_source = "student"

        if self.student_dashboard:
            self.student_dashboard.hide()

        self.search_books_view = SearchBooksView(self)
        self.auth_controller.search_books_view = self.search_books_view
        self.search_books_view.show()
        self.load_all_books_for_search()

    def load_all_books_for_search(self):
        books = BookModel.get_all_books()
        if self.search_books_view:
            self.search_books_view.populate_table(books)

    def search_books_action(self):
        if not self.search_books_view:
            return

        keyword = self.search_books_view.search_input.text().strip()

        if not keyword:
            self.load_all_books_for_search()
            return

        books = BookModel.search_books(keyword)
        self.search_books_view.populate_table(books)

    def back_to_librarian_dashboard_from_search(self):
        if self.search_books_view:
            self.search_books_view.close()
            self.search_books_view = None
            self.auth_controller.search_books_view = None

        if self.librarian_dashboard:
            self.librarian_dashboard.show()

    def back_to_student_dashboard_from_search(self):
        if self.search_books_view:
            self.search_books_view.close()
            self.search_books_view = None
            self.auth_controller.search_books_view = None

        if self.student_dashboard:
            self.student_dashboard.show()

    def close_all_views(self):
        if self.manage_books_view:
            self.manage_books_view.close()
        if self.search_books_view:
            self.search_books_view.close()