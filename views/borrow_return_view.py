from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class BorrowReturnView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selected_record_id = None
        self.setWindowTitle("Borrow / Return Books")
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
                border-radius: 22px;
            }

            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #111;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #666;
                background: transparent;
            }

            QFrame#sectionCard {
                background-color: #fafafa;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
            }

            QLabel#sectionTitle {
                font-size: 14px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }

            QLabel#miniLabel {
                font-size: 11px;
                color: #666;
                background: transparent;
            }

            QComboBox {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                color: #222;
            }

            QPushButton#borrowButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: bold;
            }

            QPushButton#borrowButton:hover {
                background-color: #2980b9;
            }

            QPushButton#returnButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: bold;
            }

            QPushButton#returnButton:hover {
                background-color: #27ae60;
            }

            QPushButton#refreshButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: bold;
            }

            QPushButton#refreshButton:hover {
                background-color: #d68910;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #7d878a;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                gridline-color: #ececec;
                color: #222;
                selection-background-color: #dbeafe;
                selection-color: #111;
            }

            QHeaderView::section {
                background-color: #111;
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
        main_card.setFixedSize(980, 640)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Borrow / Return Books")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Manage book borrowing, returns, due dates, and penalties")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_sections = QHBoxLayout()
        top_sections.setSpacing(14)

        borrow_card = QFrame()
        borrow_card.setObjectName("sectionCard")
        borrow_layout = QVBoxLayout(borrow_card)
        borrow_layout.setContentsMargins(16, 14, 16, 14)
        borrow_layout.setSpacing(10)

        borrow_title = QLabel("Borrow Book")
        borrow_title.setObjectName("sectionTitle")

        borrower_label = QLabel("Select Student")
        borrower_label.setObjectName("miniLabel")

        self.student_combo = QComboBox()

        book_label = QLabel("Select Available Book")
        book_label.setObjectName("miniLabel")

        self.book_combo = QComboBox()

        borrow_btn = QPushButton("Borrow Book")
        borrow_btn.setObjectName("borrowButton")
        borrow_btn.clicked.connect(self.controller.borrow_book)

        borrow_layout.addWidget(borrow_title)
        borrow_layout.addWidget(borrower_label)
        borrow_layout.addWidget(self.student_combo)
        borrow_layout.addWidget(book_label)
        borrow_layout.addWidget(self.book_combo)
        borrow_layout.addWidget(borrow_btn)

        return_card = QFrame()
        return_card.setObjectName("sectionCard")
        return_layout = QVBoxLayout(return_card)
        return_layout.setContentsMargins(16, 14, 16, 14)
        return_layout.setSpacing(10)

        return_title = QLabel("Return Book")
        return_title.setObjectName("sectionTitle")

        return_note = QLabel("Select a record from the table below, then click return.")
        return_note.setObjectName("miniLabel")
        return_note.setWordWrap(True)

        return_btn = QPushButton("Return Selected Book")
        return_btn.setObjectName("returnButton")
        return_btn.clicked.connect(self.controller.return_selected_book)

        refresh_btn = QPushButton("Refresh Table")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.clicked.connect(self.controller.load_borrow_return_data)

        return_layout.addWidget(return_title)
        return_layout.addWidget(return_note)
        return_layout.addStretch()
        return_layout.addWidget(return_btn)
        return_layout.addWidget(refresh_btn)

        top_sections.addWidget(borrow_card, 2)
        top_sections.addWidget(return_card, 1)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Record ID", "Student", "Book", "Borrow Date",
            "Due Date", "Return Date", "Penalty", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_borrow_return)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_sections)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def load_student_combo(self, students):
        self.student_combo.clear()
        for student in students:
            full_name = f"{student['first_name']} {student['last_name']}"
            self.student_combo.addItem(full_name, student["id"])

    def load_book_combo(self, books):
        self.book_combo.clear()
        for book in books:
            self.book_combo.addItem(book["title"], book["id"])

    def populate_table(self, records):
        self.table.clearContents()
        self.table.setRowCount(len(records))
        self.selected_record_id = None

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(record["student_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(record["book_title"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(record["borrow_date"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(record["due_date"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(record["return_date"]) if record["return_date"] else ""))
            self.table.setItem(row, 6, QTableWidgetItem(str(record["penalty"])))
            self.table.setItem(row, 7, QTableWidgetItem(record["status"]))

    def select_row(self, row, column):
        self.selected_record_id = int(self.table.item(row, 0).text())

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)