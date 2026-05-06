from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class LibrarianDashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Librarian Dashboard")
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

            QPushButton#taskCard {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                text-align: left;
                padding: 16px;
                color: #111827;
            }

            QPushButton#taskCard:hover {
                background-color: #eef2ff;
                border: 1px solid #818cf8;
            }

            QLabel#taskIcon {
                font-size: 22px;
                background: transparent;
            }

            QLabel#taskTitle {
                font-size: 14px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#taskText {
                font-size: 11px;
                color: #6b7280;
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

        role = QLabel("LIBRARIAN PANEL")
        role.setObjectName("roleLabel")

        btn_dashboard = QPushButton("Dashboard")
        btn_manage_users = QPushButton("Manage Users")
        btn_books = QPushButton("Books")
        btn_borrow_return = QPushButton("Borrow / Return")
        btn_logout = QPushButton("Logout")

        for btn in [
            btn_dashboard,
            btn_manage_users,
            btn_books,
            btn_borrow_return
        ]:
            btn.setObjectName("menuBtn")

        btn_logout.setObjectName("logoutBtn")

        side_layout.addWidget(logo)
        side_layout.addWidget(role)
        side_layout.addSpacing(20)
        side_layout.addWidget(btn_dashboard)
        side_layout.addWidget(btn_manage_users)
        side_layout.addWidget(btn_books)
        side_layout.addWidget(btn_borrow_return)
        side_layout.addStretch()
        side_layout.addWidget(btn_logout)

        btn_dashboard.clicked.connect(self.controller.refresh_dashboard_stats)
        btn_manage_users.clicked.connect(self.controller.open_manage_users)
        btn_books.clicked.connect(self.controller.open_manage_books)
        btn_borrow_return.clicked.connect(self.controller.open_borrow_return)
        btn_logout.clicked.connect(self.controller.logout)

        # ================= CONTENT =================

        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 26, 28, 26)
        content_layout.setSpacing(18)

        page_title = QLabel("Librarian Dashboard")
        page_title.setObjectName("pageTitle")

        page_subtitle = QLabel("Daily operations for borrowing, returning, users, and book inventory.")
        page_subtitle.setObjectName("pageSubtitle")

        # ================= STATS =================

        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)

        self.total_users_card = self.create_stat_card(
            "statBlue",
            "0",
            "Users",
            "Registered users"
        )

        self.total_books_card = self.create_stat_card(
            "statGreen",
            "0",
            "Books",
            "Inventory"
        )

        self.borrowed_books_card = self.create_stat_card(
            "statOrange",
            "0",
            "Borrowed",
            "Currently out"
        )

        self.overdue_books_card = self.create_stat_card(
            "statDark",
            "0",
            "Overdue",
            "Needs follow-up"
        )

        stats_row.addWidget(self.total_users_card)
        stats_row.addWidget(self.total_books_card)
        stats_row.addWidget(self.borrowed_books_card)
        stats_row.addWidget(self.overdue_books_card)

        # ================= OPERATIONS AREA =================

        lower_row = QHBoxLayout()
        lower_row.setSpacing(14)

        # LEFT: TASK CARDS
        tasks_panel = QFrame()
        tasks_panel.setObjectName("panelCard")

        tasks_layout = QVBoxLayout(tasks_panel)
        tasks_layout.setContentsMargins(20, 18, 20, 18)
        tasks_layout.setSpacing(12)

        tasks_title = QLabel("Today’s Operations")
        tasks_title.setObjectName("panelTitle")

        tasks_subtitle = QLabel("Start the most common librarian tasks quickly.")
        tasks_subtitle.setObjectName("panelSubtitle")

        task_grid = QGridLayout()
        task_grid.setHorizontalSpacing(12)
        task_grid.setVerticalSpacing(12)

        borrow_task = self.create_task_card(
            "🔁",
            "Borrow / Return",
            "Process borrowing and returns using IDs.",
            self.controller.open_borrow_return
        )

        users_task = self.create_task_card(
            "👥",
            "Manage Users",
            "Create users and update account status.",
            self.controller.open_manage_users
        )

        books_task = self.create_task_card(
            "📚",
            "Books",
            "Add, edit, search, and filter books.",
            self.controller.open_manage_books
        )

        refresh_task = self.create_task_card(
            "↻",
            "Refresh Dashboard",
            "Reload current statistics and alerts.",
            self.controller.refresh_dashboard_stats
        )

        task_grid.addWidget(borrow_task, 0, 0)
        task_grid.addWidget(users_task, 0, 1)
        task_grid.addWidget(books_task, 1, 0)
        task_grid.addWidget(refresh_task, 1, 1)

        tasks_layout.addWidget(tasks_title)
        tasks_layout.addWidget(tasks_subtitle)
        tasks_layout.addSpacing(6)
        tasks_layout.addLayout(task_grid)
        tasks_layout.addStretch()

        # RIGHT: OVERDUE FOLLOW-UP
        overdue_panel = QFrame()
        overdue_panel.setObjectName("panelCard")

        overdue_layout = QVBoxLayout(overdue_panel)
        overdue_layout.setContentsMargins(20, 18, 20, 18)
        overdue_layout.setSpacing(12)

        overdue_title = QLabel("Overdue Follow-up")
        overdue_title.setObjectName("panelTitle")

        overdue_subtitle = QLabel("Books that should be followed up today.")
        overdue_subtitle.setObjectName("panelSubtitle")

        self.overdue_list_layout = QVBoxLayout()
        self.overdue_list_layout.setSpacing(8)

        overdue_layout.addWidget(overdue_title)
        overdue_layout.addWidget(overdue_subtitle)
        overdue_layout.addSpacing(6)
        overdue_layout.addLayout(self.overdue_list_layout)
        overdue_layout.addStretch()

        lower_row.addWidget(tasks_panel, 2)
        lower_row.addWidget(overdue_panel, 1)

        # ================= NOTE =================

        note_card = QFrame()
        note_card.setObjectName("noteCard")

        note_layout = QVBoxLayout(note_card)
        note_layout.setContentsMargins(18, 14, 18, 14)
        note_layout.setSpacing(5)

        note_title = QLabel("Librarian Reminder")
        note_title.setObjectName("noteTitle")

        note_text = QLabel(
            "Borrowing requires User ID and Book ID. Returning only needs the Book ID through the return window. Inactive users cannot borrow books."
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

    def create_stat_card(self, object_name, value_text, label_text, hint_text):
        card = QFrame()
        card.setObjectName(object_name)
        card.setFixedHeight(105)

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

    def create_task_card(self, icon_text, title_text, desc_text, callback):
        button = QPushButton()
        button.setObjectName("taskCard")
        button.setMinimumHeight(118)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)

        layout = QVBoxLayout(button)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        icon = QLabel(icon_text)
        icon.setObjectName("taskIcon")

        title = QLabel(title_text)
        title.setObjectName("taskTitle")

        desc = QLabel(desc_text)
        desc.setObjectName("taskText")
        desc.setWordWrap(True)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()

        return button

    def create_overdue_item(self, book_title, user_name, late_days):
        item = QFrame()
        item.setObjectName("overdueItem")
        item.setFixedHeight(72)

        layout = QVBoxLayout(item)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(3)

        title = QLabel(str(book_title))
        title.setObjectName("overdueTitle")
        title.setWordWrap(True)

        meta = QLabel(f"{user_name}  •  {late_days} day/s overdue")
        meta.setObjectName("overdueMeta")
        meta.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(meta)

        return item

    # ================= DATA SETTERS =================

    def set_stats(self, total_users, total_books, borrowed_books, overdue_books):
        self.total_users_card.value_label.setText(str(total_users))
        self.total_books_card.value_label.setText(str(total_books))
        self.borrowed_books_card.value_label.setText(str(borrowed_books))
        self.overdue_books_card.value_label.setText(str(overdue_books))

    def set_insights(self, active_borrowed, returned_books, overdue_count, total_penalty):
        # Kept for compatibility with your controller.
        # This layout does not show insight cards anymore.
        pass

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

        for record in overdue_records[:5]:
            overdue_item = self.create_overdue_item(
                record["book_title"],
                record["student_name"],
                record["late_days"]
            )
            self.overdue_list_layout.addWidget(overdue_item)