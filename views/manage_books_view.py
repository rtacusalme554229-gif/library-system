from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ManageBooksView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selected_book_id = None

        self.setWindowTitle("Manage Books")
        self.setFixedSize(APP_WIDTH, APP_HEIGHT)

        self.setup_ui()
        center_window(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Arial;
                color: #111827;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 20px;
            }

            QFrame#formPanel {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QLabel#titleLabel {
                font-size: 25px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#fieldLabel {
                font-size: 11px;
                font-weight: bold;
                color: #374151;
                background: transparent;
            }

            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                background: white;
                color: #222;
                font-size: 12px;
            }

            QPushButton#addButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#addButton:hover {
                background-color: #16a34a;
            }

            QPushButton#updateButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#updateButton:hover {
                background-color: #0284c7;
            }

            QPushButton#deleteButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#deleteButton:hover {
                background-color: #dc2626;
            }

            QPushButton#clearButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#clearButton:hover {
                background-color: #d97706;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #7d878a;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                gridline-color: #e6e6e6;
                color: #222;
                selection-background-color: #dbeafe;
                selection-color: #111;
            }

            QHeaderView::section {
                background-color: black;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(960, 660)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(12)

        title = QLabel("Manage Books")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Add, update, delete, search, filter books, and manage copies.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, category, or status")
        self.search_input.textChanged.connect(self.controller.search_books)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Available", "Borrowed", "Lost"])
        self.filter_combo.currentTextChanged.connect(self.controller.filter_books)

        search_row.addWidget(self.search_input, 4)
        search_row.addWidget(self.filter_combo, 1)

        form_panel = QFrame()
        form_panel.setObjectName("formPanel")

        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(16, 14, 16, 14)
        form_layout.setSpacing(10)

        row_1 = QHBoxLayout()
        row_1.setSpacing(10)

        title_box = QVBoxLayout()
        title_label = QLabel("Book Title")
        title_label.setObjectName("fieldLabel")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")
        title_box.addWidget(title_label)
        title_box.addWidget(self.title_input)

        author_box = QVBoxLayout()
        author_label = QLabel("Author")
        author_label.setObjectName("fieldLabel")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author")
        author_box.addWidget(author_label)
        author_box.addWidget(self.author_input)

        row_1.addLayout(title_box)
        row_1.addLayout(author_box)

        row_2 = QHBoxLayout()
        row_2.setSpacing(10)

        category_box = QVBoxLayout()
        category_label = QLabel("Category")
        category_label.setObjectName("fieldLabel")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter category")
        category_box.addWidget(category_label)
        category_box.addWidget(self.category_input)

        copies_box = QVBoxLayout()
        copies_label = QLabel("Total Copies")
        copies_label.setObjectName("fieldLabel")
        self.copies_input = QLineEdit()
        self.copies_input.setPlaceholderText("Example: 3")
        copies_box.addWidget(copies_label)
        copies_box.addWidget(self.copies_input)

        row_2.addLayout(category_box)
        row_2.addLayout(copies_box)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        add_btn = QPushButton("Add Book")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.controller.add_book)

        update_btn = QPushButton("Update Book")
        update_btn.setObjectName("updateButton")
        update_btn.clicked.connect(self.controller.update_book)

        delete_btn = QPushButton("Delete Book")
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(self.controller.delete_book)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear_form)

        button_row.addWidget(add_btn)
        button_row.addWidget(update_btn)
        button_row.addWidget(delete_btn)
        button_row.addWidget(clear_btn)

        form_layout.addLayout(row_1)
        form_layout.addLayout(row_2)
        form_layout.addLayout(button_row)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category",
            "Total", "Available", "Borrowed", "Lost", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_books)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(search_row)
        layout.addWidget(form_panel)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def populate_table(self, books):
        self.table.clearContents()
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(book["title"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(book["author"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(book["category"] or "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(book.get("total_copies", 1))))
            self.table.setItem(row, 5, QTableWidgetItem(str(book.get("available_copies", 0))))
            self.table.setItem(row, 6, QTableWidgetItem(str(book.get("borrowed_copies", 0))))
            self.table.setItem(row, 7, QTableWidgetItem(str(book.get("lost_copies", 0))))
            self.table.setItem(row, 8, QTableWidgetItem(str(book["status"])))

    def select_row(self, row, col):
        id_item = self.table.item(row, 0)
        title_item = self.table.item(row, 1)
        author_item = self.table.item(row, 2)
        category_item = self.table.item(row, 3)
        copies_item = self.table.item(row, 4)

        if not id_item:
            return

        self.selected_book_id = int(id_item.text())

        self.title_input.setText(title_item.text() if title_item else "")
        self.author_input.setText(author_item.text() if author_item else "")
        self.category_input.setText(category_item.text() if category_item else "")
        self.copies_input.setText(copies_item.text() if copies_item else "1")

    def clear_form(self):
        self.selected_book_id = None
        self.title_input.clear()
        self.author_input.clear()
        self.category_input.clear()
        self.copies_input.clear()
        self.table.clearSelection()

    def get_form_data(self):
        return {
            "title": self.title_input.text().strip(),
            "author": self.author_input.text().strip(),
            "category": self.category_input.text().strip(),
            "total_copies": self.copies_input.text().strip()
        }

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)