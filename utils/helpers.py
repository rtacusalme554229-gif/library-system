from PyQt6.QtWidgets import QApplication


def center_window(window):
    screen = QApplication.primaryScreen().availableGeometry()
    frame = window.frameGeometry()
    frame.moveCenter(screen.center())
    window.move(frame.topLeft())