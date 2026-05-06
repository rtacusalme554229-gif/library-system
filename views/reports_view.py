from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QDateEdit, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ReportsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Library Reports")
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
                border-radius: 24px;
            }

            QFrame#heroCard {
                background-color: #111827;
                border-radius: 22px;
            }

            QLabel#heroTitle {
                color: white;
                font-size: 30px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#heroSubtitle {
                color: #d1d5db;
                font-size: 13px;
                background: transparent;
            }

            QFrame#filterCard {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QLabel#filterLabel {
                color: #374151;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }

            QDateEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 9px;
                padding: 9px;
                font-size: 12px;
                color: #111827;
            }

            QPushButton#generateButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px 18px;
                font-weight: bold;
            }

            QPushButton#generateButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#exportButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px 18px;
                font-weight: bold;
            }

            QPushButton#exportButton:hover {
                background-color: #15803d;
            }

            QPushButton#backButton {
                background-color: #111827;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #1f2937;
            }

            QFrame#previewCard {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
            }

            QLabel#previewTitle {
                font-size: 18px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#previewSubtitle {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea QWidget {
                background: transparent;
            }

            QFrame#reportSection {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QLabel#sectionTitle {
                font-size: 15px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#sectionSubtitle {
                font-size: 11px;
                color: #6b7280;
                background: transparent;
            }

            QFrame#miniCard {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }

            QLabel#miniLabel {
                font-size: 10px;
                font-weight: bold;
                color: #6b7280;
                background: transparent;
            }

            QLabel#miniValue {
                font-size: 14px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QFrame#transactionItem {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }

            QLabel#transactionTitle {
                font-size: 13px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#transactionMeta {
                font-size: 11px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#statusBorrowed {
                background-color: #fff7ed;
                color: #9a3412;
                border: 1px solid #fed7aa;
                border-radius: 9px;
                padding: 5px 9px;
                font-size: 11px;
                font-weight: bold;
            }

            QLabel#statusReturned {
                background-color: #ecfdf5;
                color: #166534;
                border: 1px solid #bbf7d0;
                border-radius: 9px;
                padding: 5px 9px;
                font-size: 11px;
                font-weight: bold;
            }

            QLabel#emptyLabel {
                background-color: #f9fafb;
                border: 1px dashed #d1d5db;
                border-radius: 12px;
                padding: 18px;
                color: #6b7280;
                font-size: 12px;
                font-weight: bold;
            }
        """)

        root = QVBoxLayout()
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(940, 650)

        main_layout = QVBoxLayout(main_card)
        main_layout.setContentsMargins(24, 22, 24, 22)
        main_layout.setSpacing(14)

        # ================= HERO =================

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero.setFixedHeight(95)

        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 16, 24, 16)
        hero_layout.setSpacing(5)

        hero_title = QLabel("Library Reports")
        hero_title.setObjectName("heroTitle")

        hero_subtitle = QLabel(
            "Generate visual summaries and export complete PDF reports."
        )
        hero_subtitle.setObjectName("heroSubtitle")

        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_subtitle)

        # ================= FILTER BAR =================

        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_card.setFixedHeight(74)

        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(18, 12, 18, 12)
        filter_layout.setSpacing(12)

        from_label = QLabel("FROM")
        from_label.setObjectName("filterLabel")

        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("MM/dd/yyyy")
        self.from_date.setDate(QDate.currentDate().addMonths(-1))

        to_label = QLabel("TO")
        to_label.setObjectName("filterLabel")

        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("MM/dd/yyyy")
        self.to_date.setDate(QDate.currentDate())

        generate_btn = QPushButton("Generate")
        generate_btn.setObjectName("generateButton")
        generate_btn.clicked.connect(self.controller.generate_admin_report)

        export_btn = QPushButton("Export PDF")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.controller.export_admin_report_pdf)

        filter_layout.addWidget(from_label)
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(to_label)
        filter_layout.addWidget(self.to_date)
        filter_layout.addStretch()
        filter_layout.addWidget(generate_btn)
        filter_layout.addWidget(export_btn)

        # ================= VISUAL PREVIEW =================

        preview_card = QFrame()
        preview_card.setObjectName("previewCard")

        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(18, 16, 18, 16)
        preview_layout.setSpacing(10)

        preview_title = QLabel("Visual Report Preview")
        preview_title.setObjectName("previewTitle")

        preview_subtitle = QLabel(
            "A dashboard-style summary. Export PDF still creates the complete report."
        )
        preview_subtitle.setObjectName("previewSubtitle")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.report_layout = QVBoxLayout(self.scroll_content)
        self.report_layout.setContentsMargins(0, 0, 0, 0)
        self.report_layout.setSpacing(12)

        # Report Info
        self.report_info_section = self.create_section(
            "Report Information",
            "Who requested the report and selected date range."
        )

        self.requested_by_card = self.create_mini_card("REQUESTED BY", "-")
        self.generated_on_card = self.create_mini_card("GENERATED ON", "-")
        self.date_range_card = self.create_mini_card("DATE RANGE", "-")

        self.add_cards_to_section(
            self.report_info_section,
            [self.requested_by_card, self.generated_on_card, self.date_range_card]
        )

        # Library Stats
        self.library_stats_section = self.create_section(
            "Library Statistics",
            "Current library records and inventory status."
        )

        self.total_books_card = self.create_mini_card("TOTAL BOOKS", "0")
        self.available_books_card = self.create_mini_card("AVAILABLE", "0")
        self.borrowed_books_card = self.create_mini_card("BORROWED", "0")
        self.total_users_card = self.create_mini_card("USERS", "0")
        self.total_librarians_card = self.create_mini_card("LIBRARIANS", "0")

        self.add_cards_to_section(
            self.library_stats_section,
            [
                self.total_books_card,
                self.available_books_card,
                self.borrowed_books_card,
                self.total_users_card,
                self.total_librarians_card
            ]
        )

        # Transaction Summary
        self.transaction_summary_section = self.create_section(
            "Transaction Summary",
            "Borrowing, return, overdue, and penalty totals."
        )

        self.transaction_count_card = self.create_mini_card("TRANSACTIONS", "0")
        self.return_count_card = self.create_mini_card("RETURNS", "0")
        self.overdue_count_card = self.create_mini_card("OVERDUE", "0")
        self.penalty_total_card = self.create_mini_card("PENALTY", "₱0.00")

        self.add_cards_to_section(
            self.transaction_summary_section,
            [
                self.transaction_count_card,
                self.return_count_card,
                self.overdue_count_card,
                self.penalty_total_card
            ]
        )

        # Recent Transactions
        self.recent_section = self.create_section(
            "Recent Transactions Preview",
            "Latest transactions from the selected date range."
        )

        self.recent_list_layout = QVBoxLayout()
        self.recent_list_layout.setSpacing(8)
        self.recent_section.content_layout.addLayout(self.recent_list_layout)

        self.report_layout.addWidget(self.report_info_section)
        self.report_layout.addWidget(self.library_stats_section)
        self.report_layout.addWidget(self.transaction_summary_section)
        self.report_layout.addWidget(self.recent_section)
        self.report_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)

        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(preview_subtitle)
        preview_layout.addWidget(self.scroll_area)

        # ================= BACK =================

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_reports)

        main_layout.addWidget(hero)
        main_layout.addWidget(filter_card)
        main_layout.addWidget(preview_card)
        main_layout.addWidget(back_btn)

        root.addWidget(main_card)
        self.setLayout(root)

    # ================= UI HELPERS =================

    def create_section(self, title_text, subtitle_text):
        section = QFrame()
        section.setObjectName("reportSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("sectionTitle")

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("sectionSubtitle")

        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(content_layout)

        section.content_layout = content_layout
        return section

    def create_mini_card(self, label_text, value_text):
        card = QFrame()
        card.setObjectName("miniCard")
        card.setFixedHeight(62)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 9, 12, 9)
        layout.setSpacing(3)

        label = QLabel(label_text)
        label.setObjectName("miniLabel")

        value = QLabel(value_text)
        value.setObjectName("miniValue")

        value.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(value)

        card.value_label = value
        return card

    def add_cards_to_section(self, section, cards):
        row = QHBoxLayout()
        row.setSpacing(8)

        for card in cards:
            row.addWidget(card)

        section.content_layout.addLayout(row)

    def create_transaction_item(self, record):
        item = QFrame()
        item.setObjectName("transactionItem")

        layout = QHBoxLayout(item)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        penalty = float(record["penalty"]) if record["penalty"] else 0
        status = str(record["status"])

        title = QLabel(str(record["book_title"]))
        title.setObjectName("transactionTitle")
        title.setWordWrap(True)

        meta = QLabel(
            f"{record['student_name']} • Borrowed: {record['borrow_date']} • "
            f"Due: {record['due_date']} • Penalty: ₱{penalty:.2f}"
        )
        meta.setObjectName("transactionMeta")
        meta.setWordWrap(True)

        text_box = QVBoxLayout()
        text_box.setSpacing(3)
        text_box.addWidget(title)
        text_box.addWidget(meta)

        status_label = QLabel(status)

        if status == "Returned":
            status_label.setObjectName("statusReturned")
        else:
            status_label.setObjectName("statusBorrowed")

        layout.addLayout(text_box)
        layout.addStretch()
        layout.addWidget(status_label)

        return item

    # ================= DATA HELPERS =================

    def get_date_range(self):
        start_date = self.from_date.date().toPyDate()
        end_date = self.to_date.date().toPyDate()
        return start_date, end_date

    # Kept for compatibility because AdminController still calls set_stats()
    def set_stats(self, total_records, returned, overdue, total_penalty):
        pass

    def set_visual_report(self, data):
        self.requested_by_card.value_label.setText(str(data.get("requested_by", "-")))
        self.generated_on_card.value_label.setText(str(data.get("generated_on", "-")))
        self.date_range_card.value_label.setText(str(data.get("date_range", "-")))

        self.total_books_card.value_label.setText(str(data.get("total_books", 0)))
        self.available_books_card.value_label.setText(str(data.get("available_books", 0)))
        self.borrowed_books_card.value_label.setText(str(data.get("borrowed_books", 0)))
        self.total_users_card.value_label.setText(str(data.get("total_users", 0)))
        self.total_librarians_card.value_label.setText(str(data.get("total_librarians", 0)))

        self.transaction_count_card.value_label.setText(str(data.get("total_transactions", 0)))
        self.return_count_card.value_label.setText(str(data.get("total_returned", 0)))
        self.overdue_count_card.value_label.setText(str(data.get("total_overdue", 0)))
        self.penalty_total_card.value_label.setText(f"₱{data.get('total_penalty', 0):.2f}")

        self.populate_recent_transactions(data.get("recent_transactions", []))

    def populate_recent_transactions(self, records):
        while self.recent_list_layout.count():
            item = self.recent_list_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not records:
            empty = QLabel("No transactions found for the selected date range.")
            empty.setObjectName("emptyLabel")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_list_layout.addWidget(empty)
            return

        for record in records[:5]:
            self.recent_list_layout.addWidget(
                self.create_transaction_item(record)
            )

    # Compatibility if older controller still calls set_report_text()
    def set_report_text(self, text):
        pass

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)