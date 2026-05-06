from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class BorrowReturnView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Borrow / Return")
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
                border: 1px solid #e5e7eb;
                border-radius: 22px;
            }

            QFrame#borrowCard {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QFrame#returnCard {
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

            QLabel#sectionTitle {
                font-size: 15px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#sectionText {
                font-size: 11px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#fieldLabel {
                font-size: 11px;
                font-weight: bold;
                color: #374151;
                background: transparent;
            }

            QLabel#lookupLabel {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 9px;
                padding: 9px;
                font-size: 12px;
                color: #111827;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 9px;
                background: white;
                color: #111827;
                font-size: 12px;
            }

            QPushButton#borrowButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#borrowButton:hover {
                background-color: #0284c7;
            }

            QPushButton#returnButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#returnButton:hover {
                background-color: #16a34a;
            }

            QPushButton#refreshButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#refreshButton:hover {
                background-color: #d97706;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 9px;
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
        main_card.setFixedSize(960, 660)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(22, 16, 22, 16)
        layout.setSpacing(10)

        title = QLabel("Borrow / Return")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Borrow using User ID and Book ID. Return using Book ID only.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================= TOP AREA =================

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        # BORROW CARD
        borrow_card = QFrame()
        borrow_card.setObjectName("borrowCard")
        borrow_card.setFixedHeight(220)

        borrow_layout = QVBoxLayout(borrow_card)
        borrow_layout.setContentsMargins(16, 12, 16, 12)
        borrow_layout.setSpacing(8)

        borrow_title = QLabel("Borrow Book")
        borrow_title.setObjectName("sectionTitle")

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        user_box = QVBoxLayout()
        user_box.setSpacing(5)

        user_label = QLabel("User ID")
        user_label.setObjectName("fieldLabel")

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter User ID")
        self.user_id_input.textChanged.connect(self.controller.lookup_borrow_fields)

        user_box.addWidget(user_label)
        user_box.addWidget(self.user_id_input)

        book_box = QVBoxLayout()
        book_box.setSpacing(5)

        book_label = QLabel("Book ID")
        book_label.setObjectName("fieldLabel")

        self.book_id_input = QLineEdit()
        self.book_id_input.setPlaceholderText("Enter Book ID")
        self.book_id_input.textChanged.connect(self.controller.lookup_borrow_fields)

        book_box.addWidget(book_label)
        book_box.addWidget(self.book_id_input)

        input_row.addLayout(user_box)
        input_row.addLayout(book_box)

        lookup_row = QHBoxLayout()
        lookup_row.setSpacing(10)

        self.user_lookup_label = QLabel("User: -")
        self.user_lookup_label.setObjectName("lookupLabel")

        self.book_lookup_label = QLabel("Book: -")
        self.book_lookup_label.setObjectName("lookupLabel")

        lookup_row.addWidget(self.user_lookup_label)
        lookup_row.addWidget(self.book_lookup_label)

        borrow_btn = QPushButton("Borrow Book")
        borrow_btn.setObjectName("borrowButton")
        borrow_btn.clicked.connect(self.controller.borrow_book_by_id)

        borrow_layout.addWidget(borrow_title)
        borrow_layout.addLayout(input_row)
        borrow_layout.addLayout(lookup_row)
        borrow_layout.addWidget(borrow_btn)

        # RETURN CARD - COMPACT
        return_card = QFrame()
        return_card.setObjectName("returnCard")
        return_card.setFixedHeight(220)
        return_card.setFixedWidth(280)

        return_layout = QVBoxLayout(return_card)
        return_layout.setContentsMargins(16, 12, 16, 12)
        return_layout.setSpacing(9)

        return_title = QLabel("Return Book")
        return_title.setObjectName("sectionTitle")

        return_text = QLabel("Open the return popup to check condition and penalty.")
        return_text.setObjectName("sectionText")
        return_text.setWordWrap(True)

        open_return_btn = QPushButton("Open Return Window")
        open_return_btn.setObjectName("returnButton")
        open_return_btn.clicked.connect(self.controller.open_return_window)

        refresh_btn = QPushButton("Refresh Table")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.clicked.connect(self.controller.load_borrow_return_data)

        return_layout.addWidget(return_title)
        return_layout.addWidget(return_text)
        return_layout.addStretch()
        return_layout.addWidget(open_return_btn)
        return_layout.addWidget(refresh_btn)

        top_row.addWidget(borrow_card)
        top_row.addWidget(return_card)

        # ================= TABLE =================

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "User", "Book", "Borrow Date", "Due Date",
            "Return Date", "Penalty", "Condition", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # ================= BACK =================

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_borrow_return)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    # ================= HELPERS =================

    def set_lookup_labels(self, user_text, book_text):
        self.user_lookup_label.setText(user_text)
        self.book_lookup_label.setText(book_text)

    def clear_borrow_inputs(self):
        self.user_id_input.clear()
        self.book_id_input.clear()
        self.user_lookup_label.setText("User: -")
        self.book_lookup_label.setText("Book: -")

    def populate_table(self, records):
        self.table.clearContents()
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            penalty = float(record["penalty"]) if record["penalty"] else 0

            self.table.setItem(row, 0, QTableWidgetItem(str(record["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(record["student_name"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(record["book_title"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(record["borrow_date"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(record["due_date"])))
            self.table.setItem(
                row,
                5,
                QTableWidgetItem(str(record["return_date"]) if record["return_date"] else "")
            )
            self.table.setItem(row, 6, QTableWidgetItem(f"₱{penalty:.2f}"))
            self.table.setItem(row, 7, QTableWidgetItem(str(record.get("book_condition", "Good"))))
            self.table.setItem(row, 8, QTableWidgetItem(str(record["status"])))

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)