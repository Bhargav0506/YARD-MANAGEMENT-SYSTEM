import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QPalette, QFont, QBrush, QIcon
from PyQt5.QtCore import Qt
from store import MainWindow as StoreWindow
from read_updated import ReadWindow as ReadWindow
from update_updated import UpdateWindow as UpdateWindow
from delete import DeleteWindow as DeleteWindow
from graph import GraphWindow as GraphWindow
from sales_graph import SalesGraphWindow as SalesGraphWindow

class LoginWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(400, 400, 400, 270)
        self.setWindowIcon(QIcon('icon.jpg'))  # Replace with your icon file path
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center-align the content vertically

        # Username field
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px; /* Increase font size */
                padding: 10px; /* Increase padding */
            }
        """)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password field
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px; /* Increase font size */
                padding: 10px; /* Increase padding */
            }
        """)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff; /* Blue color */
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                min-width: 120px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #0056b3; /* Darker blue color when pressed */
            }
            QPushButton:hover {
                background-color: #0056b3; /* Darker blue color on hover */
            }
        """)
        layout.addWidget(self.login_button)

        # Widget setup
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "pass":
            self.close()
            self.main_window.showMaximized()
        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yard Management System")

        # Create a QWidget for the top section and set its layout
        self.top_section = QWidget()
        self.top_layout = QVBoxLayout(self.top_section)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        pixmap = QPixmap('banner.png')
        self.image_label.setPixmap(pixmap)
        self.top_layout.addWidget(self.image_label)
        self.top_section.setFixedHeight(200)

        # Create the button section
        self.button_section = QWidget()
        self.button_layout = QVBoxLayout(self.button_section)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.setSpacing(20)

        # Create and style the buttons
        self.store_button = QPushButton("Store Data")
        self.read_button = QPushButton("Read Data")
        self.update_button = QPushButton("Update Data")
        self.delete_button = QPushButton("Delete Data")
        self.graphs_button = QPushButton("Production Graphs")
        self.sales_graph_button = QPushButton("Sales Graph")
        button_style = """
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                min-width: 200px;
                min-height: 50px;
                text-align: center;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

        # Apply the stylesheet to each button
        for button in [self.store_button, self.read_button, self.update_button, self.delete_button, self.graphs_button, self.sales_graph_button]:
            button.setStyleSheet(button_style)
            self.button_layout.addWidget(button)
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedSize(200, 50)

        # Create the right section for displaying windows
        self.right_section = QWidget()
        self.right_layout = QVBoxLayout(self.right_section)
        self.right_layout.setContentsMargins(10, 10, 30, 10)

        self.bg_label = QLabel(self.right_section)
        self.bg_label.setPixmap(QPixmap("icon1.png"))
        self.bg_label.setScaledContents(True)
        self.bg_label.setFixedSize(500, 500)
        
        self.right_layout.addWidget(self.bg_label)

        # Connect buttons to their respective functions
        self.store_button.clicked.connect(self.open_store_window)
        self.read_button.clicked.connect(self.open_read_window)
        self.update_button.clicked.connect(self.open_update_window)
        self.delete_button.clicked.connect(self.open_delete_window)
        self.graphs_button.clicked.connect(self.open_graphs_window)
        self.sales_graph_button.clicked.connect(self.open_sales_graph_window)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.top_section)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button_section)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(self.right_section)
        bottom_layout.setSpacing(20)
        main_layout.addLayout(bottom_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_store_window(self):
        self.clear_layout(self.right_layout)
        store_window = StoreWindow()
        store_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(store_window)

    def open_read_window(self):
        self.clear_layout(self.right_layout)
        read_window = ReadWindow()
        read_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(read_window)

    def open_update_window(self):
        self.clear_layout(self.right_layout)
        update_window = UpdateWindow()
        update_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(update_window)

    def open_delete_window(self):
        self.clear_layout(self.right_layout)
        delete_window = DeleteWindow()
        delete_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(delete_window)

    def open_graphs_window(self):
        self.clear_layout(self.right_layout)
        graph_window = GraphWindow()
        graph_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(graph_window)

    def open_sales_window(self):
        self.clear_layout(self.right_layout)
        sales_window = SalesWindow()
        sales_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(sales_window)

    def open_sales_graph_window(self):
        self.clear_layout(self.right_layout)
        sales_graph_window = SalesGraphWindow()
        sales_graph_window.setStyleSheet("background-color: white;")
        self.right_layout.addWidget(sales_graph_window)


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    login_window = LoginWindow(main_window)
    login_window.show()
    sys.exit(app.exec_())
