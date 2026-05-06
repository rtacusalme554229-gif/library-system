from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QStackedWidget
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class StudentDashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.cached_books = []
        self.cached_records = []

        self.setWindowTitle("User Dashboard")
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
                font-size: 22px;
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
                border-radius: 24px;
            }

            QLabel#pageTitle {
                font-size: 30px;
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

            QLabel#statValue {
                color: white;
                font-size: 28px;
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
                color: rgba(255,255,255,0.85);
                font-size: 10px;
                background: transparent;
            }

            QFrame#sectionCard {
                background-color: #fafafa;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
            }

            QLabel#sectionTitle {
                font-size: 17px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#sectionDesc {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QLineEdit {
                padding: 11px;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                background: white;
                color: #222;
                font-size: 12px;
            }

            QPushButton#searchButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 11px 18px;
                font-weight: bold;
            }

            QPushButton#searchButton:hover {
                background-color: #1d4ed8;
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
                background-color: #111827;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QPushButton#quickButton {
                background-color: #fafafa;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                text-align: left;
                padding: 18px;
                color: #111827;
            }

            QPushButton#quickButton:hover {
                background-color: #eef2ff;
                border: 1px solid #6366f1;
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
        side_layout.setContentsMargins(18, 22, 18, 22)
        side_layout.setSpacing(10)

        logo = QLabel("BookWise")
        logo.setObjectName("logoLabel")

        role = QLabel("USER PANEL")
        role.setObjectName("roleLabel")

        btn_dashboard = QPushButton("Dashboard")
        btn_search = QPushButton("Search Books")
        btn_history = QPushButton("My Borrowed Books")
        btn_logout = QPushButton("Logout")

        for btn in [btn_dashboard, btn_search, btn_history]:
            btn.setObjectName("menuBtn")

        btn_logout.setObjectName("logoutBtn")

        side_layout.addWidget(logo)
        side_layout.addWidget(role)
        side_layout.addSpacing(16)
        side_layout.addWidget(btn_dashboard)
        side_layout.addWidget(btn_search)
        side_layout.addWidget(btn_history)
        side_layout.addStretch()
        side_layout.addWidget(btn_logout)

        # ================= CONTENT =================
        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 26, 28, 26)

        self.stack = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.search_page = self.create_search_page()
        self.history_page = self.create_history_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.history_page)

        content_layout.addWidget(self.stack)

        root.addWidget(sidebar)
        root.addWidget(content)

        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        btn_search.clicked.connect(lambda: self.stack.setCurrentWidget(self.search_page))
        btn_history.clicked.connect(lambda: self.stack.setCurrentWidget(self.history_page))
        btn_logout.clicked.connect(self.controller.logout)

        self.stack.setCurrentWidget(self.dashboard_page)

    # ================= PAGES =================

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("User Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Search available books and monitor your borrowing history.")
        subtitle.setObjectName("pageSubtitle")

        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)

        total_card = self.create_stat_card("statBlue", "0", "Total Borrowed", "All borrowed records")
        active_card = self.create_stat_card("statOrange", "0", "Active", "Currently borrowed")
        returned_card = self.create_stat_card("statGreen", "0", "Returned", "Completed returns")

        self.total = total_card.value_label
        self.active = active_card.value_label
        self.returned = returned_card.value_label

        stats_row.addWidget(total_card)
        stats_row.addWidget(active_card)
        stats_row.addWidget(returned_card)

        quick_row = QHBoxLayout()
        quick_row.setSpacing(14)

        search_btn = self.create_quick_button(
            "Search Books",
            "Browse all available books in the library.",
            lambda: self.stack.setCurrentWidget(self.search_page)
        )

        borrowed_btn = self.create_quick_button(
            "My Borrowed Books",
            "Review borrowed, returned, and penalty records.",
            lambda: self.stack.setCurrentWidget(self.history_page)
        )

        quick_row.addWidget(search_btn)
        quick_row.addWidget(borrowed_btn)

        # Recent Activity Preview
        activity_card = QFrame()
        activity_card.setObjectName("sectionCard")

        activity_layout = QVBoxLayout(activity_card)
        activity_layout.setContentsMargins(18, 16, 18, 16)
        activity_layout.setSpacing(10)

        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("sectionTitle")

        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(3)
        self.activity_table.setHorizontalHeaderLabels(["Book", "Status", "Date"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(self.activity_table)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(stats_row)
        layout.addLayout(quick_row)
        layout.addWidget(activity_card)
        layout.addStretch()

        return page

    def create_search_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("Search Books")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Search available books by title, author, or category.")
        subtitle.setObjectName("pageSubtitle")

        card = QFrame()
        card.setObjectName("sectionCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        section_title = QLabel("Available Books")
        section_title.setObjectName("sectionTitle")

        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, category...")

        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        search_btn.clicked.connect(self.run_search)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("searchButton")
        clear_btn.clicked.connect(self.clear_search)

        search_row.addWidget(self.search_input)
        search_row.addWidget(search_btn)
        search_row.addWidget(clear_btn)

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(5)
        self.books_table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Category", "Status"])
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.books_table.verticalHeader().setVisible(False)
        self.books_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.books_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        card_layout.addWidget(section_title)
        card_layout.addLayout(search_row)
        card_layout.addWidget(self.books_table)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)

        return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        title = QLabel("My Borrowed Books")
        title.setObjectName("pageTitle")

        subtitle = QLabel("View your borrowing history, due dates, returns, penalties, and status.")
        subtitle.setObjectName("pageSubtitle")

        card = QFrame()
        card.setObjectName("sectionCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Book Title", "Borrow Date", "Due Date", "Return Date", "Penalty", "Status"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        card_layout.addWidget(self.history_table)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)

        return page

    # ================= ACTIONS =================

    def run_search(self):
        keyword = self.search_input.text().strip()
        self.controller.search_books(keyword)

    def clear_search(self):
        self.search_input.clear()
        self.controller.search_books("")

    # ================= HELPERS =================

    def create_stat_card(self, object_name, value_text, label_text, hint_text):
        card = QFrame()
        card.setObjectName(object_name)
        card.setFixedHeight(105)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

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

    def create_quick_button(self, title_text, desc_text, callback):
        button = QPushButton()
        button.setObjectName("quickButton")
        button.setMinimumHeight(125)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)

        layout = QVBoxLayout(button)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("sectionTitle")

        desc = QLabel(desc_text)
        desc.setObjectName("sectionDesc")
        desc.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()

        return button

    # ================= DATA LOADERS =================

    def set_stats(self, total, active, returned):
        self.total.setText(str(total))
        self.active.setText(str(active))
        self.returned.setText(str(returned))

    def populate_books_table(self, books):
        self.cached_books = books

        self.books_table.clearContents()
        self.books_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.books_table.setItem(row, 0, QTableWidgetItem(str(book["id"])))
            self.books_table.setItem(row, 1, QTableWidgetItem(str(book["title"])))
            self.books_table.setItem(row, 2, QTableWidgetItem(str(book["author"])))
            self.books_table.setItem(row, 3, QTableWidgetItem(str(book["category"] or "")))
            self.books_table.setItem(row, 4, QTableWidgetItem(str(book["status"])))

    def populate_table(self, records):
        self.cached_records = records

        self.history_table.clearContents()
        self.history_table.setRowCount(len(records))

        for row, record in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(str(record["book_title"])))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(record["borrow_date"])))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(record["due_date"])))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(record["return_date"]) if record["return_date"] else ""))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(record["penalty"])))
            self.history_table.setItem(row, 5, QTableWidgetItem(str(record["status"])))

        self.populate_activity(records)

    def populate_activity(self, records):
        self.activity_table.clearContents()
        self.activity_table.setRowCount(min(5, len(records)))

        for row, record in enumerate(records[:5]):
            date_value = record["return_date"] if record["return_date"] else record["borrow_date"]

            self.activity_table.setItem(row, 0, QTableWidgetItem(str(record["book_title"])))
            self.activity_table.setItem(row, 1, QTableWidgetItem(str(record["status"])))
            self.activity_table.setItem(row, 2, QTableWidgetItem(str(date_value)))