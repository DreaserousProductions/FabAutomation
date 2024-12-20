import sys
import os
import math
from config import GUI_STYLE, DRAG_DROP_AREA_STYLE, PROGRESS_STYLE, TAGS, PRICES, CATEGORIES, TEXTURE_CATEGORIES
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEventLoop, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
                            QComboBox, QTextEdit, QHBoxLayout, QCheckBox, QProgressBar, QApplication)
from automation import (automate_listing_creation, automate_listing_creation_bulk,
                        automate_listing_edit, automate_listing_edit_bulk, bulk_draft_deletion)

# --- Worker Thread ---
class AutomationWorker(QThread):
    status_signal = pyqtSignal(str)  # Signal to send status updates
    progress_signal = pyqtSignal(float)  # Signal to send status updates
    finished_signal = pyqtSignal()   # Signal to indicate completion

    def __init__(self, headless, folder_path, auto_option, desc_text, cat_text, tags, price, pro_price, add_desc, submit_for_review, product_type):
        super().__init__()
        # Initialize worker parameters
        self.headless = headless
        self.folder_path = folder_path
        self.auto_option = auto_option
        self.desc_text = desc_text
        self.cat_text = cat_text
        self.product_type = product_type
        self.tags = tags
        self.price = price
        self.pro_price = pro_price
        self.add_desc = add_desc
        self.submit_for_review = submit_for_review

    def run(self):
        try:
            # Emit status update indicating the task is starting
            self.status_signal.emit("Running automation...")
            
            if self.auto_option == "Upload Single Model":
                automate_listing_creation(self.headless, self.folder_path, self.desc_text, self.cat_text, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review, self.product_type)
            elif self.auto_option == "Upload Multiple Models":
                automate_listing_creation_bulk(self.headless, self.folder_path, self.desc_text, self.cat_text, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review, self.product_type, self.progress_signal)
            elif self.auto_option == "Edit Model":
                automate_listing_edit(self.headless, self.folder_path, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review)
            elif self.auto_option == "Edit Multiple Models":
                automate_listing_edit_bulk(self.headless, self.folder_path, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review, self.progress_signal)
            elif self.auto_option == "Bulk Delete":
                bulk_draft_deletion(self.headless)

            # Emit status update indicating the task is completed
            self.status_signal.emit("Automation completed!")
        except Exception as e:
            # Emit error message if an exception occurs
            self.status_signal.emit(f"Error: {str(e)}")
        finally:
            # Emit finished signal when task is done
            self.finished_signal.emit()

# --- Custom Widgets ---
class TagComboBox(QComboBox):
    tag_added = pyqtSignal()

    def __init__(self, tags, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.tags = tags
        self.addItems(self.tags)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.tag_added.emit()
        else:
            super().keyPressEvent(event)

class FolderDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.folder_path = ""
        self.files = []
        self.folder_label = QLabel("Drop a folder here", self)
        self.folder_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        self.setLayout(layout)
        self.setStyleSheet(DRAG_DROP_AREA_STYLE)

    def setStyle(self):
        self.setStyleSheet()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.folder_path = folder_path
                self.files = os.listdir(folder_path)
                self.folder_label.setText(f"Folder: {folder_path}\n{len(self.files)} items found.")

# --- Main GUI ---
class AutomationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration variables
        self.automation_option = "Upload Single Model"
        self.category_option = ""
        self.product_type = "3D Model"
        self.selected_tags = []
        self.submit_for_review = False
        self.headless_mode = False

        # Data constants
        self.tags = TAGS
        self.prices = PRICES

        # GUI setup
        self.setStyleSheet(GUI_STYLE)
        self.setWindowTitle("Fab Automation Worker")
        self.setGeometry(100, 100, 1000, 200)
        self.worker_thread = None

        self.init_ui()

    # --- Initialization ---
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add sections
        self.create_dropdown_section(main_layout)
        main_layout.addSpacing(10)
        self.create_product_dropdown_section(main_layout)
        main_layout.addSpacing(10)
        self.create_description_section(main_layout)
        self.create_category_section(main_layout)
        main_layout.addSpacing(20)
        self.create_tag_section(main_layout)
        main_layout.addSpacing(20)
        self.create_price_section(main_layout)
        main_layout.addSpacing(20)
        self.create_texture_description_section(main_layout)
        self.create_folder_section(main_layout)
        self.create_submit_review_checkbox(main_layout)
        main_layout.addSpacing(5)
        self.create_headless_checkbox(main_layout)
        main_layout.addSpacing(50)
        self.create_progress_bar(main_layout)
        self.create_buttons_section(main_layout)
        main_layout.addStretch()

    # --- UI Sections ---
    def create_dropdown_section(self, layout):
        self.automation_dropdown = QComboBox()
        self.automation_dropdown.addItems(
            ["Upload Single Model", "Upload Multiple Models", "Edit Model", "Edit Multiple Models", "Bulk Delete"]
        )
        self.automation_dropdown.currentIndexChanged.connect(self.update_ui)
        layout.addWidget(self.automation_dropdown)

    def create_product_dropdown_section(self, layout):
        self.product_dropdown = QComboBox()
        self.product_dropdown.addItems(["Select Product Category", "3D Model", "Textures"])
        self.product_dropdown.currentIndexChanged.connect(self.update_product_type)
        layout.addWidget(self.product_dropdown)

    def create_description_section(self, layout):
        self.description_label = QLabel("Enter model Description:")
        self.description_textbox = QTextEdit()
        self.description_textbox.setPlaceholderText("Type description here...")
        self.description_textbox.setMinimumHeight(100)

        layout.addWidget(self.description_label)
        layout.addWidget(self.description_textbox)

    def create_category_section(self, layout):
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(CATEGORIES)
        self.category_dropdown.currentIndexChanged.connect(self.update_category_option)
        layout.addWidget(self.category_dropdown)

    def create_tag_section(self, layout):
        self.tag_dropdown = TagComboBox(self.tags, self)
        self.tag_dropdown.tag_added.connect(self.add_or_remove_tag)
        self.selected_tags_label = QLabel("Selected Tags: None")

        layout.addWidget(self.tag_dropdown)
        layout.addWidget(self.selected_tags_label)

    def create_price_section(self, layout):
        horizontal_pricebox = QHBoxLayout()
        price_vBox = QVBoxLayout()
        professional_price_vBox = QVBoxLayout()

        self.personal_price_label = QLabel("Enter personal price:")
        self.personal_price_dropdown = QComboBox()
        self.personal_price_dropdown.addItems(self.prices)

        self.professional_price_label = QLabel("Enter professional price:")
        self.professional_price_dropdown = QComboBox()
        self.professional_price_dropdown.addItems(self.prices)

        price_vBox.addWidget(self.personal_price_label)
        price_vBox.addWidget(self.personal_price_dropdown)
        professional_price_vBox.addWidget(self.professional_price_label)
        professional_price_vBox.addWidget(self.professional_price_dropdown)

        horizontal_pricebox.addLayout(price_vBox)
        horizontal_pricebox.addSpacing(20)
        horizontal_pricebox.addLayout(professional_price_vBox)

        layout.addLayout(horizontal_pricebox)

    def create_texture_description_section(self, layout):
        self.texture_label = QLabel("Enter additional files Description:")
        self.texture_textbox = QTextEdit()
        self.texture_textbox.setPlaceholderText("Type description here...")
        self.texture_textbox.setMinimumHeight(50)

        layout.addWidget(self.texture_label)
        layout.addWidget(self.texture_textbox)

    def create_folder_section(self, layout):
        self.folder_drop_widget = FolderDropWidget()
        layout.addWidget(self.folder_drop_widget)

    def create_submit_review_checkbox(self, layout):
        self.submit_review_checkbox = QCheckBox("Submit for Review")
        self.submit_review_checkbox.stateChanged.connect(self.toggle_submit_review)
        layout.addWidget(self.submit_review_checkbox)

    def create_headless_checkbox(self, layout):
        self.headless_checkbox = QCheckBox("Headless Mode")
        self.headless_checkbox.stateChanged.connect(self.toggle_headless_mode)
        layout.addWidget(self.headless_checkbox)

    def create_progress_bar(self, layout):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)  # Minimum value
        self.progress_bar.setMaximum(1000)  # Maximum value
        self.progress_bar.setValue(0) 
        self.progress_bar.setStyleSheet(PROGRESS_STYLE)
        layout.addWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

    def create_buttons_section(self, layout):
        button_layout = QHBoxLayout()

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("status-label")
        button_layout.addWidget(self.status_label)

        button_layout.addStretch()

        self.start_button = QPushButton("Start Automation")
        self.start_button.setMaximumWidth(300)
        self.start_button.setObjectName("s-btn")
        self.start_button.clicked.connect(lambda: self.start_automation_process(layout))
        button_layout.addWidget(self.start_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setMaximumWidth(300)
        self.quit_button.setObjectName("q-btn")
        self.quit_button.clicked.connect(self.close)
        button_layout.addWidget(self.quit_button)

        layout.addLayout(button_layout)

    # --- Functional Methods ---
    def update_ui(self):
        self.automation_option = self.automation_dropdown.currentText()
        is_bulk_delete = self.automation_option == "Bulk Delete"
        is_edit_model = self.automation_option == "Edit Model"
        is_edit_multiple_model = self.automation_option == "Edit Multiple Models"

        # Adjust visibility based on the selected option
        self.description_label.setVisible(not is_bulk_delete and not is_edit_model and not is_edit_multiple_model)
        self.description_textbox.setVisible(not is_bulk_delete and not is_edit_model and not is_edit_multiple_model)
        self.category_dropdown.setVisible(not is_bulk_delete and not is_edit_model and not is_edit_multiple_model)
        self.product_dropdown.setVisible(not is_bulk_delete and not is_edit_model and not is_edit_multiple_model)
        self.tag_dropdown.setVisible(not is_bulk_delete)
        self.selected_tags_label.setVisible(not is_bulk_delete)
        self.personal_price_label.setVisible(not is_bulk_delete)
        self.personal_price_dropdown.setVisible(not is_bulk_delete)
        self.professional_price_label.setVisible(not is_bulk_delete)
        self.professional_price_dropdown.setVisible(not is_bulk_delete)
        self.texture_label.setVisible(not is_bulk_delete)
        self.texture_textbox.setVisible(not is_bulk_delete)
        self.submit_review_checkbox.setVisible(not is_bulk_delete)

    def add_or_remove_tag(self):
        selected_tag = self.tag_dropdown.currentText()
        if selected_tag in self.selected_tags:
            self.selected_tags.remove(selected_tag)
        elif selected_tag != "Select Tags" and len(self.selected_tags) <= 15:
            self.selected_tags.append(selected_tag)
        self.update_selected_tags_label()

    def update_selected_tags_label(self):
        tags_display = ", ".join(self.selected_tags) if self.selected_tags else "None"
        self.selected_tags_label.setText(f"Selected Tags: {tags_display}")

    def start_automation_process(self, layout):
        folder_path = self.folder_drop_widget.folder_path
        description_text = self.description_textbox.toPlainText()
        if not folder_path or not self.category_option:
            if self.automation_option == 'Bulk Delete' or self.automation_option == 'Edit Multiple Models':
                ...
            else:
                self.status_label.setText("Missing required fields.")
                return

        self.worker_thread = AutomationWorker(
            self.headless_mode, folder_path, self.automation_option,
            description_text, self.category_option, self.selected_tags,
            self.personal_price_dropdown.currentText(),
            self.professional_price_dropdown.currentText(),
            self.texture_textbox.toPlainText(), self.submit_for_review,
            self.product_type
        )
        
        if self.automation_option == 'Upload Multiple Models' or self.automation_option == 'Edit Multiple Models':
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)

        self.worker_thread.status_signal.connect(self.update_status_label)
        self.worker_thread.progress_signal.connect(self.update_progress_bar)
        self.worker_thread.start()

    def update_status_label(self, message):
        self.status_label.setText(message)

    def toggle_submit_review(self, state):
        self.submit_for_review = state == Qt.Checked

    def toggle_headless_mode(self, state):
        self.headless_mode = state == Qt.Checked

    def update_category_option(self):
        if self.category_dropdown.currentText() != "Select Category":
            self.category_option = self.category_dropdown.currentText()

    def update_product_type(self):
        self.product_type = self.product_dropdown.currentText() if self.product_dropdown.currentText() != "Select Product Category" else "3D Model"
        if(self.product_type == "3D Model"):
            self.category_dropdown.clear()
            self.category_dropdown.addItems(CATEGORIES)
        else:
            self.category_dropdown.clear()
            self.category_dropdown.addItems(TEXTURE_CATEGORIES)

    def update_progress_bar(self, progress):
        target_value = round(progress * 1000)
        duration = 3000  # 3 seconds
        start_value = self.progress_bar.value()
        step_count = 0
        total_steps = 100  # 100 steps for smooth transition
        
        # Easing function (ease-in-out)
        def ease_in_out(t):
            return t * t * (3 - 2 * t)

        def step():
            nonlocal step_count
            t = step_count / total_steps
            eased_t = ease_in_out(t)
            new_value = round(start_value + (target_value - start_value) * eased_t)
            self.progress_bar.setValue(new_value)
            QApplication.processEvents()  # Ensure the UI updates during the loop
            
            step_count += 1
            if step_count > total_steps:
                self.timer.stop()

        # Set up a QTimer to periodically update the progress bar
        self.timer = QTimer()
        self.timer.timeout.connect(step)
        self.timer.start(duration // total_steps) 

def main():
    app = QApplication(sys.argv)
    gui = AutomationGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()