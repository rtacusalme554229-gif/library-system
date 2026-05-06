from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox,
    QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt
from utils.helpers import center_window


class ReturnBookView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Return Book")
        self.setFixedSize(540, 620)

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

            QLabel#titleLabel {
                font-size: 24px;
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
                font-size: 12px;
                font-weight: bold;
                color: #374151;
                background: transparent;
            }

            QLineEdit, QComboBox {
                padding: 11px;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                background: white;
                color: #111827;
                font-size: 13px;
            }

            QTextEdit {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 12px;
                font-size: 12px;
                color: #111827;
            }

            QPushButton#lookupButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: bold;
            }

            QPushButton#lookupButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#returnButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 13px;
                font-weight: bold;
            }

            QPushButton#returnButton:hover {
                background-color: #15803d;
            }

            QPushButton#closeButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 13px;
                font-weight: bold;
            }

            QPushButton#closeButton:hover {
                background-color: #7d878a;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(480, 570)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(10)

        title = QLabel("Return Book")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Enter the Book ID, check the record, then choose the return condition.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)

        # ================= BOOK ID =================

        book_label = QLabel("Book ID")
        book_label.setObjectName("fieldLabel")

        book_row = QHBoxLayout()
        book_row.setSpacing(8)

        self.book_id_input = QLineEdit()
        self.book_id_input.setPlaceholderText("Enter borrowed Book ID")
        self.book_id_input.textChanged.connect(self.controller.lookup_return_book)

        lookup_btn = QPushButton("Lookup")
        lookup_btn.setObjectName("lookupButton")
        lookup_btn.setFixedWidth(85)
        lookup_btn.clicked.connect(self.controller.lookup_return_book)

        book_row.addWidget(self.book_id_input)
        book_row.addWidget(lookup_btn)

        # ================= CONDITION =================

        condition_label = QLabel("Book Condition")
        condition_label.setObjectName("fieldLabel")

        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["Good", "Damaged", "Lost"])

        # ================= DETAILS =================

        details_label = QLabel("Return Details")
        details_label.setObjectName("fieldLabel")

        self.details_output = QTextEdit()
        self.details_output.setReadOnly(True)
        self.details_output.setFixedHeight(150)
        self.details_output.setText("Borrowed record details will appear here.")

        # ================= BUTTONS =================

        return_btn = QPushButton("Return Book")
        return_btn.setObjectName("returnButton")
        return_btn.setFixedHeight(44)
        return_btn.clicked.connect(self.controller.return_book_by_book_id)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedHeight(44)
        close_btn.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)

        layout.addWidget(book_label)
        layout.addLayout(book_row)

        layout.addWidget(condition_label)
        layout.addWidget(self.condition_combo)

        layout.addWidget(details_label)
        layout.addWidget(self.details_output)

        layout.addSpacing(6)
        layout.addWidget(return_btn)
        layout.addWidget(close_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    # ================= HELPERS =================

    def get_condition(self):
        return self.condition_combo.currentText()

    def set_details_text(self, text):
        self.details_output.setText(text)

    def clear_input(self):
        self.book_id_input.clear()
        self.condition_combo.setCurrentText("Good")
        self.details_output.setText("Borrowed record details will appear here.")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)