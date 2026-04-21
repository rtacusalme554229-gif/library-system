import sys
from PyQt6.QtWidgets import QApplication
from controllers.auth_controller import AuthController


def main():
    app = QApplication(sys.argv)

    controller = AuthController()
    controller.show_login()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()