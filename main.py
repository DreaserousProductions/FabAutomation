import os
from dotenv import load_dotenv, set_key
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton

from gui import main as MainGUI  # Assuming your main GUI class is in gui.py

def set_env_variable(env_file_path, key, value):
    with open(env_file_path, 'a') as env_file:
        env_file.write(f'{key}="{value}"\n')

class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FAB Automation Setup")
        self.setGeometry(100, 100, 300, 100)

        # Create input fields for environment variables
        self.user_data_label = QLabel("Enter your PC User:", self)
        self.user_data_input = QLineEdit(self)
        self.user_data_input.setPlaceholderText("Enter your user here...")

        self.scroll_lim_label = QLabel("Enter Scroll Limit:", self)
        self.scroll_lim_input = QLineEdit(self)
        self.scroll_lim_input.setPlaceholderText("Enter your scroll limit here...")

        # Save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_env)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.user_data_label)
        layout.addWidget(self.user_data_input)
        layout.addWidget(self.scroll_lim_label)
        layout.addWidget(self.scroll_lim_input)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_env(self):
        USER_DATA = self.user_data_input.text()
        SCROLL_LIM = self.scroll_lim_input.text()

        if USER_DATA:
            # Write the .env file
            env_file_path = '.env'
            set_env_variable(env_file_path, 'USER_DATA_DIR', f"C:/Users/{USER_DATA}/AppData/Local/Google/Chrome/User Data")
            set_env_variable(env_file_path, 'SCROLL_LIMIT', SCROLL_LIM)
            set_env_variable(env_file_path, 'USER_AGENT', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

            print(f"Environment variables saved!")
            self.close()  # Close the setup window after saving


def main():
    # Initialize the QApplication
    app = QApplication([])

    # Check if .env exists
    if not os.path.exists('.env'):
        # Show setup window
        setup_window = SetupWindow()
        setup_window.show()
        app.exec_()
    
    else:
        # Launch the main application
        main_window = MainGUI()  # Replace `MainGUI` with your actual main GUI class
        main_window.show()
        app.exec_()


if __name__ == '__main__':
    main()
