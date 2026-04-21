from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ReportsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Reports")
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

            QFrame#statCardBlue {
                background-color: #3fa9f5;
                border-radius: 12px;
            }

            QFrame#statCardGreen {
                background-color: #2ecc71;
                border-radius: 12px;
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

            QLabel#statTitle {
                color: white;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#statValue {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }

            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                background: white;
                color: #222;
                padding: 10px;
                font-size: 12px;
            }

            QPushButton#generateButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#generateButton:hover {
                background-color: #222;
            }

            QPushButton#pdfButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#pdfButton:hover {
                background-color: #a93226;
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
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(900, 560)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("BookWise Reports")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Administrative Reports Overview")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)

        self.books_card = self.create_stat_card("statCardBlue", "Total Books", "0")
        self.members_card = self.create_stat_card("statCardGreen", "Total Members", "0")

        stats_row.addWidget(self.books_card)
        stats_row.addWidget(self.members_card)

        self.report_output = QTextEdit()
        self.report_output.setReadOnly(True)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        generate_btn = QPushButton("Generate Report")
        generate_btn.setObjectName("generateButton")
        generate_btn.clicked.connect(self.controller.generate_admin_report)

        pdf_btn = QPushButton("Export Clean PDF")
        pdf_btn.setObjectName("pdfButton")
        pdf_btn.clicked.connect(self.controller.export_admin_report_pdf)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_reports)

        button_row.addWidget(generate_btn)
        button_row.addWidget(pdf_btn)
        button_row.addStretch()
        button_row.addWidget(back_btn)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(stats_row)
        layout.addWidget(self.report_output)
        layout.addLayout(button_row)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def create_stat_card(self, object_name, title_text, value_text):
        card = QFrame()
        card.setObjectName(object_name)
        card.setFixedHeight(70)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)

        title = QLabel(title_text)
        title.setObjectName("statTitle")

        value = QLabel(value_text)
        value.setObjectName("statValue")

        layout.addWidget(title)
        layout.addWidget(value)

        card.value_label = value
        return card

    def set_stats(self, total_books, total_members):
        self.books_card.value_label.setText(str(total_books))
        self.members_card.value_label.setText(str(total_members))

    def set_report_text(self, text):
        self.report_output.clear()
        self.report_output.setPlainText(text)

    def get_report_text(self):
        return self.report_output.toPlainText()