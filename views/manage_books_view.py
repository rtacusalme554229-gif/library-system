from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox
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
                color: #222;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 20px;
            }

            QFrame#sectionCard {
                background-color: #fafafa;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
            }

            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #666;
                background: transparent;
            }

            QLabel#sectionTitle {
                font-size: 14px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }

            QLabel#fieldLabel {
                font-size: 11px;
                font-weight: bold;
                color: #555;
                background: transparent;
            }

            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                color: #222;
            }

            QPushButton#addButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#addButton:hover {
                background-color: #27ae60;
            }

            QPushButton#updateButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#updateButton:hover {
                background-color: #2980b9;
            }

            QPushButton#deleteButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#deleteButton:hover {
                background-color: #c0392b;
            }

            QPushButton#clearButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#clearButton:hover {
                background-color: #d68910;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
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
        main_card.setFixedSize(930, 650)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Manage Books")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Add, update, delete, and organize library books")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Book details section =====
        form_card = QFrame()
        form_card.setObjectName("sectionCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 14, 16, 14)
        form_layout.setSpacing(10)

        form_title = QLabel("Book Details")
        form_title.setObjectName("sectionTitle")

        form_row_1 = QHBoxLayout()
        form_row_1.setSpacing(10)

        title_col = QVBoxLayout()
        title_col.setSpacing(5)
        title_label = QLabel("Book Title")
        title_label.setObjectName("fieldLabel")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")
        title_col.addWidget(title_label)
        title_col.addWidget(self.title_input)

        author_col = QVBoxLayout()
        author_col.setSpacing(5)
        author_label = QLabel("Author")
        author_label.setObjectName("fieldLabel")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        author_col.addWidget(author_label)
        author_col.addWidget(self.author_input)

        form_row_1.addLayout(title_col)
        form_row_1.addLayout(author_col)

        form_row_2 = QHBoxLayout()
        form_row_2.setSpacing(10)

        category_col = QVBoxLayout()
        category_col.setSpacing(5)
        category_label = QLabel("Category")
        category_label.setObjectName("fieldLabel")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter category")
        category_col.addWidget(category_label)
        category_col.addWidget(self.category_input)

        status_col = QVBoxLayout()
        status_col.setSpacing(5)
        status_label = QLabel("Book Status")
        status_label.setObjectName("fieldLabel")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Available", "Borrowed"])
        status_col.addWidget(status_label)
        status_col.addWidget(self.status_combo)

        form_row_2.addLayout(category_col, 3)
        form_row_2.addLayout(status_col, 1)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        add_btn = QPushButton("Add Book")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.controller.save_book)

        update_btn = QPushButton("Update Book")
        update_btn.setObjectName("updateButton")
        update_btn.clicked.connect(self.controller.update_book)

        delete_btn = QPushButton("Delete Book")
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(self.controller.delete_book)

        clear_btn = QPushButton("Clear Form")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear_form)

        button_row.addWidget(add_btn)
        button_row.addWidget(update_btn)
        button_row.addWidget(delete_btn)
        button_row.addWidget(clear_btn)

        form_layout.addWidget(form_title)
        form_layout.addLayout(form_row_1)
        form_layout.addLayout(form_row_2)
        form_layout.addLayout(button_row)

        # ===== Table filter section =====
        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        filter_title = QLabel("Show Books:")
        filter_title.setObjectName("fieldLabel")

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Available", "Borrowed"])
        self.filter_combo.currentIndexChanged.connect(lambda: self.controller.filter_books())

        filter_row.addWidget(filter_title)
        filter_row.addWidget(self.filter_combo)
        filter_row.addStretch()

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Category", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.load_selected_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_books)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(form_card)
        layout.addLayout(filter_row)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def populate_table(self, books):
        self.table.clearContents()
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(book["title"]))
            self.table.setItem(row, 2, QTableWidgetItem(book["author"]))
            self.table.setItem(row, 3, QTableWidgetItem(book["category"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(book["status"]))

    def load_selected_row(self, row, column):
        self.selected_book_id = int(self.table.item(row, 0).text())
        self.title_input.setText(self.table.item(row, 1).text())
        self.author_input.setText(self.table.item(row, 2).text())
        self.category_input.setText(self.table.item(row, 3).text())
        self.status_combo.setCurrentText(self.table.item(row, 4).text())

    def clear_form(self):
        self.selected_book_id = None
        self.title_input.clear()
        self.author_input.clear()
        self.category_input.clear()
        self.status_combo.setCurrentText("Available")

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)