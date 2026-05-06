from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ClickableFrame(QFrame):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback

    def mousePressEvent(self, event):
        if self.callback:
            self.callback()
        super().mousePressEvent(event)


class AdminDashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Admin Dashboard")
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

            QFrame#sidebar {
                background-color: #111827;
            }

            QLabel#logoLabel {
                color: white;
                font-size: 23px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#roleLabel {
                color: #9ca3af;
                font-size: 11px;
                font-weight: bold;
                background: transparent;
            }

            QPushButton#menuBtn {
                color: white;
                background-color: transparent;
                padding: 13px;
                text-align: left;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }

            QPushButton#menuBtn:hover {
                background-color: #1f2937;
            }

            QPushButton#logoutBtn {
                color: white;
                background-color: #dc2626;
                padding: 13px;
                text-align: center;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }

            QPushButton#logoutBtn:hover {
                background-color: #b91c1c;
            }

            QFrame#content {
                background-color: white;
                border-top-left-radius: 24px;
                border-bottom-left-radius: 24px;
            }

            QLabel#pageTitle {
                font-size: 32px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#pageSubtitle {
                font-size: 13px;
                color: #6b7280;
                background: transparent;
            }

            QFrame#statBlue {
                background-color: #2563eb;
                border-radius: 18px;
            }

            QFrame#statGreen {
                background-color: #16a34a;
                border-radius: 18px;
            }

            QFrame#statOrange {
                background-color: #f59e0b;
                border-radius: 18px;
            }

            QFrame#statDark {
                background-color: #111827;
                border-radius: 18px;
            }

            QLabel#statValue {
                color: white;
                font-size: 29px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#statLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#statHint {
                color: rgba(255,255,255,0.86);
                font-size: 10px;
                background: transparent;
            }

            QFrame#panelCard {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
            }

            QLabel#panelTitle {
                font-size: 17px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#panelSubtitle {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QFrame#insightItem {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
            }

            QLabel#insightIcon {
                font-size: 18px;
                background: transparent;
            }

            QLabel#insightLabel {
                font-size: 11px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#insightValue {
                font-size: 15px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QFrame#overdueItem {
                background-color: #fff7ed;
                border: 1px solid #fed7aa;
                border-radius: 14px;
            }

            QLabel#overdueTitle {
                font-size: 13px;
                font-weight: bold;
                color: #7c2d12;
                background: transparent;
            }

            QLabel#overdueMeta {
                font-size: 11px;
                color: #9a3412;
                background: transparent;
            }

            QLabel#emptyOverdue {
                background-color: #ecfdf5;
                border: 1px solid #bbf7d0;
                border-radius: 14px;
                padding: 16px;
                color: #166534;
                font-size: 13px;
                font-weight: bold;
            }

            QFrame#noteCard {
                background-color: #eef2ff;
                border: 1px solid #c7d2fe;
                border-radius: 18px;
            }

            QLabel#noteTitle {
                font-size: 14px;
                font-weight: bold;
                color: #3730a3;
                background: transparent;
            }

            QLabel#noteText {
                font-size: 12px;
                color: #4338ca;
                background: transparent;
            }
        """)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(18, 24, 18, 22)
        side_layout.setSpacing(10)

        logo = QLabel("BookWise")
        logo.setObjectName("logoLabel")

        role = QLabel("ADMIN PANEL")
        role.setObjectName("roleLabel")

        btn_dashboard = QPushButton("Dashboard")
        btn_accounts = QPushButton("Manage Accounts")
        btn_inventory = QPushButton("Inventory Books")
        btn_reports = QPushButton("Reports")
        btn_logout = QPushButton("Logout")

        for btn in [btn_dashboard, btn_accounts, btn_inventory, btn_reports]:
            btn.setObjectName("menuBtn")

        btn_logout.setObjectName("logoutBtn")

        side_layout.addWidget(logo)
        side_layout.addWidget(role)
        side_layout.addSpacing(20)
        side_layout.addWidget(btn_dashboard)
        side_layout.addWidget(btn_accounts)
        side_layout.addWidget(btn_inventory)
        side_layout.addWidget(btn_reports)
        side_layout.addStretch()
        side_layout.addWidget(btn_logout)

        btn_dashboard.clicked.connect(self.controller.refresh_dashboard_stats)
        btn_accounts.clicked.connect(self.controller.open_manage_members)
        btn_inventory.clicked.connect(self.controller.open_admin_inventory)
        btn_reports.clicked.connect(self.controller.open_reports)
        btn_logout.clicked.connect(self.controller.logout)

        # ================= CONTENT =================

        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 26, 28, 26)
        content_layout.setSpacing(18)

        page_title = QLabel("Admin Dashboard")
        page_title.setObjectName("pageTitle")

        page_subtitle = QLabel("A clean overview of library inventory, members, borrowing activity, and reports.")
        page_subtitle.setObjectName("pageSubtitle")

        # ================= STAT CARDS =================

        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)

        self.books_card = self.create_stat_card(
            "statBlue",
            "0",
            "Total Books",
            "Library inventory",
            self.controller.open_admin_inventory
        )

        self.available_card = self.create_stat_card(
            "statGreen",
            "0",
            "Available",
            "Ready to borrow",
            self.controller.open_admin_inventory
        )

        self.borrowed_card = self.create_stat_card(
            "statOrange",
            "0",
            "Borrowed",
            "Active borrow records",
            self.controller.open_reports
        )

        self.members_card = self.create_stat_card(
            "statDark",
            "0",
            "Members",
            "Users + librarians",
            self.controller.open_manage_members
        )

        stats_row.addWidget(self.books_card)
        stats_row.addWidget(self.available_card)
        stats_row.addWidget(self.borrowed_card)
        stats_row.addWidget(self.members_card)

        # ================= MAIN LOWER AREA =================

        lower_row = QHBoxLayout()
        lower_row.setSpacing(14)

        # -------- LEFT PANEL: INSIGHTS --------

        insights_card = QFrame()
        insights_card.setObjectName("panelCard")

        insights_layout = QVBoxLayout(insights_card)
        insights_layout.setContentsMargins(20, 18, 20, 18)
        insights_layout.setSpacing(12)

        insight_title = QLabel("Library Insights")
        insight_title.setObjectName("panelTitle")

        insight_subtitle = QLabel("Quick system summary without opening reports.")
        insight_subtitle.setObjectName("panelSubtitle")

        self.most_borrowed_item = self.create_insight_item("📘", "Most Borrowed Book", "-")
        self.active_borrow_item = self.create_insight_item("🔁", "Active Borrowed Books", "0")
        self.overdue_cases_item = self.create_insight_item("⚠", "Overdue Cases", "0")
        self.penalty_item = self.create_insight_item("₱", "Total Penalty", "₱0.00")

        insights_layout.addWidget(insight_title)
        insights_layout.addWidget(insight_subtitle)
        insights_layout.addSpacing(6)
        insights_layout.addWidget(self.most_borrowed_item)
        insights_layout.addWidget(self.active_borrow_item)
        insights_layout.addWidget(self.overdue_cases_item)
        insights_layout.addWidget(self.penalty_item)
        insights_layout.addStretch()

        # -------- RIGHT PANEL: OVERDUE SUMMARY --------

        overdue_card = QFrame()
        overdue_card.setObjectName("panelCard")

        overdue_layout = QVBoxLayout(overdue_card)
        overdue_layout.setContentsMargins(20, 18, 20, 18)
        overdue_layout.setSpacing(12)

        overdue_title = QLabel("Overdue Summary")
        overdue_title.setObjectName("panelTitle")

        overdue_subtitle = QLabel("Books that need attention from the librarian.")
        overdue_subtitle.setObjectName("panelSubtitle")

        self.overdue_list_layout = QVBoxLayout()
        self.overdue_list_layout.setSpacing(8)

        overdue_layout.addWidget(overdue_title)
        overdue_layout.addWidget(overdue_subtitle)
        overdue_layout.addSpacing(6)
        overdue_layout.addLayout(self.overdue_list_layout)
        overdue_layout.addStretch()

        lower_row.addWidget(insights_card, 1)
        lower_row.addWidget(overdue_card, 1)

        # ================= BOTTOM NOTE =================

        note_card = QFrame()
        note_card.setObjectName("noteCard")

        note_layout = QVBoxLayout(note_card)
        note_layout.setContentsMargins(18, 14, 18, 14)
        note_layout.setSpacing(5)

        note_title = QLabel("Admin Note")
        note_title.setObjectName("noteTitle")

        note_text = QLabel(
            "Use Manage Accounts for librarian/user access. Use Reports for full transaction history, penalties, and PDF exports."
        )
        note_text.setObjectName("noteText")
        note_text.setWordWrap(True)

        note_layout.addWidget(note_title)
        note_layout.addWidget(note_text)

        content_layout.addWidget(page_title)
        content_layout.addWidget(page_subtitle)
        content_layout.addLayout(stats_row)
        content_layout.addLayout(lower_row)
        content_layout.addWidget(note_card)
        content_layout.addStretch()

        root.addWidget(sidebar)
        root.addWidget(content)

    # ================= UI HELPERS =================

    def create_stat_card(self, object_name, value_text, label_text, hint_text, callback):
        card = ClickableFrame(callback)
        card.setObjectName(object_name)
        card.setFixedHeight(105)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(5)

        value = QLabel(value_text)
        value.setObjectName("statValue")

        label = QLabel(label_text)
        label.setObjectName("statLabel")

        hint = QLabel(hint_text)
        hint.setObjectName("statHint")

        layout.addWidget(value)
        layout.addWidget(label)
        layout.addWidget(hint)
        layout.addStretch()

        card.value_label = value
        return card

    def create_insight_item(self, icon_text, label_text, value_text):
        item = QFrame()
        item.setObjectName("insightItem")
        item.setFixedHeight(64)

        row = QHBoxLayout(item)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(12)

        icon = QLabel(icon_text)
        icon.setObjectName("insightIcon")
        icon.setFixedWidth(28)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)

        label = QLabel(label_text)
        label.setObjectName("insightLabel")

        value = QLabel(value_text)
        value.setObjectName("insightValue")

        text_box.addWidget(label)
        text_box.addWidget(value)

        row.addWidget(icon)
        row.addLayout(text_box)
        row.addStretch()

        item.value_label = value
        return item

    def create_overdue_item(self, book_title, user_name, late_days):
        item = QFrame()
        item.setObjectName("overdueItem")
        item.setFixedHeight(70)

        layout = QVBoxLayout(item)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(3)

        title = QLabel(str(book_title))
        title.setObjectName("overdueTitle")

        meta = QLabel(f"{user_name}  •  {late_days} day/s overdue")
        meta.setObjectName("overdueMeta")

        layout.addWidget(title)
        layout.addWidget(meta)

        return item

    # ================= DATA SETTERS =================

    def set_stats(self, total_books, available_books, borrowed_books, total_members):
        self.books_card.value_label.setText(str(total_books))
        self.available_card.value_label.setText(str(available_books))
        self.borrowed_card.value_label.setText(str(borrowed_books))
        self.members_card.value_label.setText(str(total_members))

    def set_insights(self, most_borrowed, active_borrowed, overdue_count, total_penalty):
        self.most_borrowed_item.value_label.setText(str(most_borrowed))
        self.active_borrow_item.value_label.setText(str(active_borrowed))
        self.overdue_cases_item.value_label.setText(str(overdue_count))
        self.penalty_item.value_label.setText(f"₱{total_penalty:.2f}")

    def set_overdue_books(self, overdue_records):
        while self.overdue_list_layout.count():
            item = self.overdue_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not overdue_records:
            empty = QLabel("No overdue books today.")
            empty.setObjectName("emptyOverdue")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.overdue_list_layout.addWidget(empty)
            return

        for record in overdue_records[:4]:
            overdue_item = self.create_overdue_item(
                record["book_title"],
                record["student_name"],
                record["late_days"]
            )
            self.overdue_list_layout.addWidget(overdue_item)