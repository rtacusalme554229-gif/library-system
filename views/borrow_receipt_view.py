from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from utils.helpers import center_window


class BorrowReceiptView(QWidget):
    def __init__(self, receipt_data):
        super().__init__()
        self.receipt_data = receipt_data
        self.setWindowTitle("Borrow Receipt")
        self.setFixedSize(460, 760)
        self.setup_ui()
        center_window(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Arial;
                color: #1f2937;
            }

            QFrame#receiptCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 18px;
            }

            QLabel#brandLabel {
                font-size: 22px;
                font-weight: bold;
                color: #1f2937;
                background: transparent;
            }

            QLabel#subLabel {
                font-size: 11px;
                color: #7c8a96;
                background: transparent;
            }

            QLabel#fieldLabel {
                font-size: 11px;
                font-weight: bold;
                color: #53606b;
                background: transparent;
            }

            QLabel#fieldValue {
                font-size: 12px;
                color: #1f2937;
                background: #f9fafb;
                padding: 7px 10px;
                border-radius: 6px;
            }

            QLabel#dueDate {
                font-size: 12px;
                font-weight: bold;
                color: #ef4444;
                background: #fff5f5;
                padding: 7px 10px;
                border-radius: 6px;
            }

            QFrame#line {
                background-color: #d9d9d9;
                min-height: 1px;
                max-height: 1px;
            }

            QFrame#noticeBox {
                background-color: #fef3e6;
                border-left: 3px solid #f59e0b;
                border-radius: 8px;
            }

            QLabel#noticeLabel {
                font-size: 11px;
                color: #c26b00;
                background: transparent;
            }

            QPushButton#pdfButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#pdfButton:hover {
                background-color: #c0392b;
            }

            QPushButton#closeButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#closeButton:hover {
                background-color: #7f8c8d;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("receiptCard")
        card.setFixedSize(390, 700)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(10)

        brand = QLabel("📚 LIBRARY SYSTEM")
        brand.setObjectName("brandLabel")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Book Borrow Receipt")
        sub.setObjectName("subLabel")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line_top = QFrame()
        line_top.setObjectName("line")

        layout.addWidget(brand)
        layout.addWidget(sub)
        layout.addWidget(line_top)

        layout.addWidget(self.make_field("Receipt No:", self.receipt_data["receipt_no"]))
        layout.addWidget(self.make_field("Transaction Date:", self.receipt_data["transaction_date"]))

        line_mid = QFrame()
        line_mid.setObjectName("line")
        layout.addWidget(line_mid)

        layout.addWidget(self.make_field("Member ID:", self.receipt_data["member_id"]))
        layout.addWidget(self.make_field("Member Name:", self.receipt_data["student_name"]))
        layout.addWidget(self.make_field("Book ID:", self.receipt_data["book_id"]))
        layout.addWidget(self.make_field("Book Title:", self.receipt_data["book_title"]))
        layout.addWidget(self.make_field("Borrow Date:", self.receipt_data["borrow_date"]))
        layout.addWidget(self.make_field("Due Date:", self.receipt_data["due_date"], due=True))
        layout.addWidget(self.make_field("Processed By:", self.receipt_data["librarian_name"]))

        notice_box = QFrame()
        notice_box.setObjectName("noticeBox")
        notice_layout = QVBoxLayout(notice_box)
        notice_layout.setContentsMargins(10, 8, 10, 8)

        notice = QLabel("⚠ Please return the book by the due date.\nLate returns incur a penalty of ₱10 per day.")
        notice.setObjectName("noticeLabel")
        notice.setWordWrap(True)

        notice_layout.addWidget(notice)
        layout.addWidget(notice_box)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        pdf_btn = QPushButton("🧾 SAVE AS PDF")
        pdf_btn.setObjectName("pdfButton")
        pdf_btn.clicked.connect(self.save_as_pdf)

        close_btn = QPushButton("✔ CLOSE")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)

        button_row.addWidget(pdf_btn)
        button_row.addWidget(close_btn)

        layout.addStretch()
        layout.addLayout(button_row)

        root_layout.addWidget(card)
        self.setLayout(root_layout)

    def make_field(self, label_text, value_text, due=False):
        wrapper = QFrame()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(4)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")

        value = QLabel(str(value_text))
        value.setWordWrap(True)
        value.setObjectName("dueDate" if due else "fieldValue")

        wrapper_layout.addWidget(label)
        wrapper_layout.addWidget(value)
        return wrapper

    def save_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Receipt as PDF",
            f"{self.receipt_data['receipt_no']}.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        html_content = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #1f2937;
                        margin: 30px;
                    }}
                    h1 {{
                        text-align: center;
                        font-size: 24px;
                        margin-bottom: 0;
                    }}
                    .sub {{
                        text-align: center;
                        color: #7c8a96;
                        font-size: 12px;
                        margin-top: 2px;
                        margin-bottom: 18px;
                    }}
                    .line {{
                        border-top: 1px solid #d1d5db;
                        margin: 12px 0 18px 0;
                    }}
                    .row {{
                        margin-bottom: 10px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #53606b;
                        font-size: 12px;
                    }}
                    .value {{
                        font-size: 13px;
                        margin-top: 2px;
                    }}
                    .due {{
                        color: #ef4444;
                        font-weight: bold;
                    }}
                    .notice {{
                        margin-top: 18px;
                        padding: 12px;
                        background: #fef3e6;
                        color: #c26b00;
                        border-left: 4px solid #f59e0b;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <h1>LIBRARY MANAGEMENT SYSTEM</h1>
                <div class="sub">Official Borrowing Receipt</div>
                <div class="line"></div>

                <div class="row"><div class="label">Receipt No:</div><div class="value">{self.receipt_data['receipt_no']}</div></div>
                <div class="row"><div class="label">Transaction Date:</div><div class="value">{self.receipt_data['transaction_date']}</div></div>
                <div class="line"></div>

                <div class="row"><div class="label">Member ID:</div><div class="value">{self.receipt_data['member_id']}</div></div>
                <div class="row"><div class="label">Member Name:</div><div class="value">{self.receipt_data['student_name']}</div></div>
                <div class="row"><div class="label">Book ID:</div><div class="value">{self.receipt_data['book_id']}</div></div>
                <div class="row"><div class="label">Book Title:</div><div class="value">{self.receipt_data['book_title']}</div></div>
                <div class="row"><div class="label">Borrow Date:</div><div class="value">{self.receipt_data['borrow_date']}</div></div>
                <div class="row"><div class="label">Due Date:</div><div class="value due">{self.receipt_data['due_date']}</div></div>
                <div class="row"><div class="label">Processed By:</div><div class="value">{self.receipt_data['librarian_name']}</div></div>

                <div class="notice">
                    Please return the book by the due date. Late returns incur a penalty of ₱10 per day.
                </div>
            </body>
        </html>
        """

        document = QTextDocument()
        document.setHtml(html_content)

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)

        document.print(printer)

        QMessageBox.information(self, "Saved", f"Receipt saved as PDF:\n{file_path}")