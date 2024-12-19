import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QComboBox, QTextEdit, QHBoxLayout, QCheckBox, QProgressBar, QApplication
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEventLoop, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from automation import automate_listing_creation, automate_listing_edit, bulk_draft_deletion

# --- Worker Thread ---
class AutomationWorker(QThread):
    status_signal = pyqtSignal(str)  # Signal to send status updates
    finished_signal = pyqtSignal()   # Signal to indicate completion

    def __init__(self, headless, folder_path, auto_option, desc_text, cat_text, tags, price, pro_price, add_desc, submit_for_review):
        super().__init__()
        # Initialize worker parameters
        self.headless = headless
        self.folder_path = folder_path
        self.auto_option = auto_option
        self.desc_text = desc_text
        self.cat_text = cat_text
        self.tags = tags
        self.price = price
        self.pro_price = pro_price
        self.add_desc = add_desc
        self.submit_for_review = submit_for_review

    def run(self):
        try:
            # Emit status update indicating the task is starting
            self.status_signal.emit("Running automation...")
            
            if self.auto_option == "Upload Single 3D Model" or self.auto_option == "Upload Multiple 3D Model":
                # Call the automation function for model upload
                automate_listing_creation(self.headless, self.folder_path, self.desc_text, self.cat_text, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review)
            elif self.auto_option == "Bulk Delete":
                # Call the bulk deletion function
                bulk_draft_deletion(self.headless)
            elif self.auto_option == "Edit Model":
                automate_listing_edit(self.headless, self.folder_path, self.tags, self.price, self.pro_price, self.add_desc, self.submit_for_review)

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
        self.setStyle()

    def setStyle(self):
        self.setStyleSheet("""
            QWidget {
                border-radius: 5px;
                border: 1px solid rgba(200, 200, 200, 0.8);
                background-color: rgba(200, 200, 200, 0.25);
                padding: 40px 80px 40px 80px;
            }
        """)

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
        self.auto_option = "Upload Single 3D Model"
        self.cat_option = ""
        self.selected_tags = []
        self.tags = self.initialize_tags()
        self.prices = self.initialize_prices()
        self.submit_for_rev = False
        self.headless = False
        self.setStyleSheet("""
            QMainWindow {
                background: #3a3a3a;
            }

            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 700;
            }
                           
            QLabel#status-label {
                font-size: 16px;
            }
            
            QComboBox {
                background: rgba(100, 100, 100, 0.5);
                color: white;
                font-size: 14px;
                font-weight: 700;
                padding: 5px 5px 5px 5px;
                border-radius: 2px;
            }
            
            QTextEdit {
                color: white;
                border-radius: 5px;
                border: 1px solid rgba(200, 200, 200, 1);
                background: rgba(20, 20, 20, 0.8);
            }
            
            QCheckBox {
                color: white;
                letter-spacing: 2px;
                font-size: 16px;
                font-weight: 400;
            }
                           
            QPushButton {
                padding: 10px 0 10px;
                min-width: 250px;
                color: white;
                border: 1px double gray;
                border-radius: 5px;
                
                font-family: "Roboto";
                font-size: 16px;
                font-weight: 900;
            }
                           
            QPushButton#s-btn {
                background: rgba(0, 180, 20, 0.8);
            }
                           
            QPushButton#q-btn {
                background: rgb(250, 40, 40);
            }
        """)
        self.init_ui()

    # --- Initialization Methods ---
    def initialize_tags(self):
        return ['Abandoned', 'Abbey', 'Abdomen', 'Aberdeenshire', 'Abies', 'Ability', 'Abomination', 'Aboriginal', 'Absorber', 'Abstract', 'Acacia', 'Academy', 'Acanthus', 'Accent', 'Accessibility', 'Accessory', 'Accident', 'Accord', 'Accordion', 'Accounting', 'Baby', 'Babylon', 'Babylonian', 'Back', 'Background', 'Backhoe', 'Backlight', 'Backpack', 'Backroom', 'Backup', 'Backwall', 'Backyard', 'Bacon', 'Bacteria', 'Badge', 'Badger', 'Badlands', 'Bag', 'Bagel', 'Baggy', 'Cab', 'Cabbage', 'Cabin', 'Cabinet', 'Cable', 'Cacao', 'Cactus', 'Cad', 'Caddy', 'Caesar', 'Cafe', 'Cafeteria', 'Cage', 'Cairn', 'Cairo', 'Cake', 'Calamari', 'Calavera', 'Calculator', 'Caldera', 'Dace', 'Dachshund', 'Dacia', 'Dacian', 'Dacite', 'Dad', 'Daemon', 'Dagger', 'Daily', 'Dairy', 'Daisy', 'Dakar', 'Dali', 'Dallas', 'Dalmatian', 'Dam', 'Damage', 'Damaged', 'Damascus', 'Damp', 'Eagle', 'Ear', 'Earbuds', 'Early', 'Earphone', 'Earring', 'Earth', 'Earthenware', 'Earthquake', 'East', 'Easter', 'Easteregg', 'Eastern', 'Eat', 'Ebony', 'Echinoderm', 'Echinoid', 'Echo', 'Eclipse', 'Ecology', 'Fable', 'Fabric', 'Fabrication', 'Fabricmaking', 'Facade', 'Face', 'Facial', 'Facility', 'Faction', 'Factory', 'Faded', 'Fail', 'Fair', 'Fairy', 'Fairytale', 'Faith', 'Fake', 'Falchion', 'Falcon', 'Fall', 'Gabbro', 'Gable', 'Gadget', 'Gaea', 'Gaia', 'Gala', 'Galactic', 'Galaxy', 'Galleon', 'Gallery', 'Gallon', 'Galvanized', 'Gambling', 'Gamepad', 'Gameplay', 'Gamer', 'Gameready', 'Gaming', 'Ganesha', 'Gang', 'Habitat', 'Habitation', 'Hack', 'Hacker', 'Hades', 'Hadrosaur', 'Hair', 'Hairband', 'Haircut', 'Hairdresser', 'Hairdressing', 'Hairdryer', 'Hairless', 'Hairpin', 'Hairstyle', 'Hairy', 'Halberd', 'Half', 'Halfpipe', 'Hall', 'Iberian', 'Ice', 'Iceage', 'Icecream', 'Iceland', 'Icelandic', 'Ichnofossil', 'Ichthyology', 'Ichthyosaur', 'Icicle', 'Icing', 'Icon', 'Iconic', 'Iconography', 'Icosahedron', 'Idea', 'Ideal', 'Identity', 'Idle', 'Idol', 'Jackal', 'Jacket', 'Jackolantern', 'Jacuzzi', 'Jade', 'Jagged', 'Jaguar', 'Jail', 'Jakarta', 'Jam', 'January', 'Japan', 'Japanese', 'Japonica', 'Japonicus', 'Jar', 'Java', 'Javanese', 'Javelin', 'Jaw', 'Kabuto', 'Kaiju', 'Kaiser', 'Kalash', 'Kalba', 'Kangaroo', 'Kansas', 'Kanto', 'Kappa', 'Karabiner', 'Karambit', 'Karate', 'Karkala', 'Karma', 'Karst', 'Katana', 'Kathmandu', 'Kawaii', 'Kayak', 'Kazakhstan', 'Label', 'Laboratory', 'Lace', 'Lacquered', 'Ladder', 'Ladieswear', 'Ladle', 'Lady', 'Lagoon', 'Lake', 'Lamancha', 'Lamb', 'Lamp', 'Lamppost', 'Lampshade', 'Lance', 'Lancer', 'Land', 'Landing', 'Landscape', 'Macaw', 'Mace', 'Machete', 'Machine', 'Machinegun', 'Machinery', 'Macro', 'Madagascar', 'Madeira', 'Madness', 'Madrid', 'Mafia', 'Magazine', 'Mage', 'Magic', 'Magical', 'Magma', 'Magnet', 'Magnetic', 'Magnificent', 'Nail', 'Name', 'Nameplate', 'Namforsen', 'Nanite', 'Nano', 'Nanotechnology', 'Nantes', 'Napkin', 'Naples', 'Napoleon', 'Napoleonic', 'Narrow', 'Nation', 'National', 'Native', 'Natural', 'Nature', 'Nautical', 'Nautiloid', 'Oak', 'Oakland', 'Oar', 'Oasis', 'Oat', 'Obelisk', 'Obese', 'Object', 'Objective', 'Oblivion', 'Observation', 'Observatory', 'Observer', 'Obsidian', 'Obstacle', 'Ocarina', 'Occipital', 'Occlusion', 'Occult', 'Ocean', 'Pacific', 'Pack', 'Package', 'Packaging', 'Packet', 'Packing', 'Pad', 'Padded', 'Paddle', 'Pagan', 'Page', 'Pagoda', 'Paid', 'Pail', 'Pain', 'Painkiller', 'Paint', 'Paintball', 'Paintbrush', 'Painted', 'Qatar', 'Qi', 'Qing', 'Quad', 'Quadcopter', 'Quadruped', 'Quantum', 'Quarantine', 'Quarry', 'Quarter', 'Quartz', 'Quartzite', 'Quaternary', 'Quay', 'Quebec', 'Queen', 'Queensland', 'Quern', 'Quest', 'Question', 'Rabbit', 'Raccoon', 'Race', 'Racecar', 'Racer', 'Racetrack', 'Racing', 'Rack', 'Racket', 'Racoon', 'Radar', 'Radial', 'Radiant', 'Radiation', 'Radiator', 'Radimlja', 'Radio', 'Radioactive', 'Radiolaria', 'Radiology', 'Saber', 'Sabertooth', 'Sable', 'Sac', 'Sachet', 'Sack', 'Sacral', 'Sacred', 'Sacrifice', 'Sacrum', 'Sad', 'Saddle', 'Safari', 'Safe', 'Safety', 'Saga', 'Sage', 'Sagittarius', 'Sago', 'Sahara', 'Tab', 'Tabernacle', 'Table', 'Tablecloth', 'Tablet', 'Tabletennis', 'Tabletop', 'Tabouret', 'Tabulate', 'Tac', 'Tackle', 'Taco', 'Tactical', 'Tactile', 'Taekwondo', 'Tag', 'Tahiti', 'Tai', 'Tail', 'Tailor', 'Uae', 'Uav', 'Ube', 'Udim', 'Ufo', 'Uganda', 'Ugly', 'Ukraine', 'Ukulele', 'Ulna', 'Ultimate', 'Ultra', 'Umbrella', 'Unbranded', 'Uncle', 'Unconformity', 'Undead', 'Underground', 'Underpass', 'Underwater', 'Vacation', 'Vaccine', 'Vacuum', 'Vale', 'Valencia', 'Valenciana', 'Valentine', 'Valhalla', 'Valkyrie', 'Valley', 'Vampire', 'Van', 'Vancouver', 'Vandal', 'Vandalism', 'Vangogh', 'Vanilla', 'Vanity', 'Vapor', 'Vaporwave', 'Wacky', 'Wadi', 'Wafer', 'Waffle', 'Wagon', 'Waist', 'Waistcoat', 'Waiter', 'Waiting', 'Waitingroom', 'Waitress', 'Wake', 'Wakizashi', 'Wales', 'Walk', 'Walkcycle', 'Walker', 'Walkietalkie', 'Walkway', 'Wall', 'Xenolith', 'Xian', 'Xray', 'Yacht', 'Yak', 'Yakuza', 'Yamato', 'Yang', 'Yankee', 'Yard', 'Yarn', 'Yayoi', 'Year', 'Yellow', 'Yeti', 'Yin', 'Yoga', 'Yogurt', 'Yokai', 'York', 'Yorkshire', 'Yosemite', 'Young', 'Zaragoza', 'Zealand', 'Zebra', 'Zen', 'Zeppelin', 'Zeus', 'Zhou', 'Zinc', 'Zip', 'Zircon', 'Zodiac', 'Zombie', 'Zone', 'Zoo', 'Zoology', 'Zoom', 'Zoomorphic', 'Zucchini', 'Zurich', 'Zweihander']
    
    def initialize_categories(self):
        return ["Buildings & Architecture", "Characters & Creatures", "Clothing & Jewelry", "Electronics & Technology", "Food & Drink", "Furniture & Fixtures", "Nature & Plants", "Scenes", "Tools, Objects & Decor", "Vehicles & Transportation", "Weapons & Combat"]

    def initialize_prices(self):
        return ["0.0 (USD)", "0.99 (USD)", "1.99 (USD)", "2.99 (USD)", "3.99 (USD)", "4.99 (USD)", "5.99 (USD)", "6.99 (USD)", "7.99 (USD)", "8.99 (USD)", "9.99 (USD)", "10.99 (USD)", "11.99 (USD)", "12.99 (USD)", "13.99 (USD)", "14.99 (USD)", "15.99 (USD)", "16.99 (USD)", "17.99 (USD)", "18.99 (USD)", "19.99 (USD)", "20.99 (USD)", "21.99 (USD)", "22.99 (USD)", "23.99 (USD)", "24.99 (USD)", "25.99 (USD)", "26.99 (USD)", "27.99 (USD)", "28.99 (USD)", "29.99 (USD)", "30.99 (USD)", "31.99 (USD)", "32.99 (USD)", "33.99 (USD)", "34.99 (USD)", "35.99 (USD)", "36.99 (USD)", "37.99 (USD)", "38.99 (USD)", "39.99 (USD)", "40.99 (USD)", "41.99 (USD)", "42.99 (USD)", "43.99 (USD)", "44.99 (USD)", "45.99 (USD)", "46.99 (USD)", "47.99 (USD)", "48.99 (USD)", "49.99 (USD)", "50.99 (USD)", "51.99 (USD)", "52.99 (USD)", "53.99 (USD)", "54.99 (USD)", "55.99 (USD)", "56.99 (USD)", "57.99 (USD)", "58.99 (USD)", "59.99 (USD)", "60.99 (USD)", "61.99 (USD)", "62.99 (USD)", "63.99 (USD)", "64.99 (USD)", "65.99 (USD)", "66.99 (USD)", "67.99 (USD)", "68.99 (USD)", "69.99 (USD)", "70.99 (USD)", "71.99 (USD)", "72.99 (USD)", "73.99 (USD)", "74.99 (USD)", "75.99 (USD)", "76.99 (USD)", "77.99 (USD)", "78.99 (USD)", "79.99 (USD)", "80.99 (USD)", "81.99 (USD)", "82.99 (USD)", "83.99 (USD)", "84.99 (USD)", "85.99 (USD)", "86.99 (USD)", "87.99 (USD)", "88.99 (USD)", "89.99 (USD)", "90.99 (USD)", "91.99 (USD)", "92.99 (USD)", "93.99 (USD)", "94.99 (USD)", "95.99 (USD)", "96.99 (USD)", "97.99 (USD)", "98.99 (USD)", "99.99 (USD)", "104.99 (USD)", "109.99 (USD)", "114.99 (USD)", "119.99 (USD)", "124.99 (USD)", "129.99 (USD)", "134.99 (USD)", "139.99 (USD)", "144.99 (USD)", "149.99 (USD)", "159.99 (USD)", "169.99 (USD)", "179.99 (USD)", "189.99 (USD)", "199.99 (USD)", "209.99 (USD)", "219.99 (USD)", "229.99 (USD)", "239.99 (USD)", "249.99 (USD)", "274.99 (USD)", "299.99 (USD)", "324.99 (USD)", "349.99 (USD)", "374.99 (USD)", "399.99 (USD)", "424.99 (USD)", "449.99 (USD)", "474.99 (USD)", "499.99 (USD)", "599.99 (USD)", "699.99 (USD)", "799.99 (USD)", "899.99 (USD)", "999.99 (USD)", "1099.99 (USD)", "1199.99 (USD)", "1299.99 (USD)", "1399.99 (USD)", "1499.99 (USD)"]


    def init_ui(self):
        self.setWindowTitle("Fab Automation Worker")
        self.setGeometry(100, 100, 1000, 200)
        self.worker_thread = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.create_dropdown_section(layout)
        self.create_description_section(layout)
        self.create_category_section(layout)
        layout.addSpacing(20)
        self.create_tag_section(layout)
        layout.addSpacing(20)
        self.create_price_section(layout)
        layout.addSpacing(20)
        self.create_add_description_section(layout)
        self.create_folder_section(layout)
        self.create_submit_checkbox(layout)
        layout.addSpacing(5)
        self.create_headless_checkbox(layout)
        layout.addSpacing(50)
        self.create_buttons_section(layout)
        layout.addStretch()

    # --- UI Sections ---
    def create_dropdown_section(self, layout):
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Upload Single 3D Model", "Upload Multiple 3D Model", "Edit Model", "Bulk Delete"])
        self.dropdown.currentIndexChanged.connect(self.update_ui)
        layout.addWidget(self.dropdown)

    def create_description_section(self, layout):
        self.label = QLabel("Enter model Description:")
        layout.addWidget(self.label)

        self.textbox = QTextEdit()
        self.textbox.setPlaceholderText("Type description here...")
        self.textbox.setMinimumHeight(100)
        layout.addWidget(self.textbox)

    def create_category_section(self, layout):
        self.cat_dropdown = QComboBox()
        self.cat_dropdown.addItem("Select Category")
        self.cat_dropdown.addItems(self.initialize_categories())
        self.cat_dropdown.currentIndexChanged.connect(self.update_category)
        layout.addWidget(self.cat_dropdown)

    def create_tag_section(self, layout):
        self.tag_dropdown = TagComboBox(self.tags, self)
        self.tag_dropdown.tag_added.connect(self.add_tag)
        layout.addWidget(self.tag_dropdown)

        self.selected_tags_label = QLabel("Selected Tags: None")
        layout.addWidget(self.selected_tags_label)

    def create_price_section(self, layout):
        self.price_label = QLabel("Enter personal price:")
        layout.addWidget(self.price_label)

        self.price_dropdown = QComboBox()
        self.price_dropdown.addItems(self.prices)
        layout.addWidget(self.price_dropdown)

        layout.addSpacing(20)

        self.pro_price_label = QLabel("Enter professional price:")
        layout.addWidget(self.pro_price_label)

        self.pro_price_dropdown = QComboBox()
        self.pro_price_dropdown.addItems(self.prices)
        layout.addWidget(self.pro_price_dropdown)

    def create_add_description_section(self, layout):
        self.add_label = QLabel("Enter Texture Description:")
        layout.addWidget(self.add_label)

        self.add_textbox = QTextEdit()
        self.add_textbox.setPlaceholderText("Type description here...")
        self.add_textbox.setMinimumHeight(50)
        layout.addWidget(self.add_textbox)

    def create_folder_section(self, layout):
        self.folder_drop_widget = FolderDropWidget()
        layout.addWidget(self.folder_drop_widget)

    def create_submit_checkbox(self, layout):
        self.checkbox = QCheckBox("Submit for Review")
        self.checkbox.stateChanged.connect(self.on_checkbox_toggled)
        layout.addWidget(self.checkbox)

    def create_headless_checkbox(self, layout):
        self.hcheckbox = QCheckBox("Headless Mode")
        self.hcheckbox.stateChanged.connect(self.headless_toggle)
        layout.addWidget(self.hcheckbox)

    def create_buttons_section(self, layout):
        hbox = QHBoxLayout()

        hbox.addStretch()
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("status-label")
        hbox.addWidget(self.status_label)
        
        hbox.addStretch()

        self.start_button = QPushButton("Start Automation")
        self.start_button.setMaximumWidth(300)
        self.start_button.clicked.connect(lambda: self.start_automation(layout))
        self.start_button.setObjectName("s-btn")
        hbox.addWidget(self.start_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setMaximumWidth(300)
        self.quit_button.clicked.connect(self.close)
        self.quit_button.setObjectName("q-btn")
        hbox.addWidget(self.quit_button)

        layout.addLayout(hbox)

    # --- Functional Methods ---
    def add_tag(self):
        selected_tag = self.tag_dropdown.currentText()
        if selected_tag != "Select Tags" and selected_tag not in self.selected_tags and len(self.selected_tags) <= 15:
            self.selected_tags.append(selected_tag)
            self.update_selected_tags_display()
        elif selected_tag in self.selected_tags:
            self.selected_tags.remove(selected_tag)
            self.update_selected_tags_display()

    def update_selected_tags_display(self):
        self.selected_tags_label.setText(f"Selected Tags: {', '.join(self.selected_tags)}")

    def periodic_function(self, current_value, dir_len):
        if(self.progress_bar.value() < current_value // dir_len):
            self.progress_bar.setValue(current_value + 1)
            QApplication.processEvents()

    def start_automation(self, layout):
        automaton = self.dropdown.currentText()
        folder_path = self.folder_drop_widget.folder_path
        desc_text = self.textbox.toPlainText()
        if automaton != 'Bulk Delete' and (not folder_path or not self.cat_option):
            self.status_label.setText("Missing required fields.")
            if automaton == 'Edit Model' and folder_path:
                ...
            else:
                return

        if automaton == 'Upload Single 3D Model' or automaton == 'Edit Model' or automaton == 'Bulk Delete':
            self.worker_thread = AutomationWorker(self.headless, folder_path, self.auto_option, desc_text, self.cat_option, self.selected_tags, self.price_dropdown.currentText(), self.pro_price_dropdown.currentText(), self.add_textbox.toPlainText(), self.submit_for_rev)
            self.worker_thread.status_signal.connect(self.update_status)
            self.worker_thread.start()
        
        else:
            dir_len = len([dir for root, dirs, files in os.walk(folder_path) for dir in dirs])
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setRange(0, 1000)
            self.progress_bar.setValue(0)
            layout.addWidget(self.progress_bar)

            for root, dirs, files in os.walk(folder_path):
                for dir_name in dirs:
                    folder_path = f"{root}/{dir_name}"
                    self.worker_thread = AutomationWorker(self.headless, folder_path, self.auto_option, desc_text, self.cat_option, self.selected_tags, self.price_dropdown.currentText(), self.pro_price_dropdown.currentText(), self.add_textbox.toPlainText(), self.submit_for_rev)
                    self.worker_thread.status_signal.connect(self.update_status)
                    
                    current_value = self.progress_bar.value()
                    QApplication.processEvents()

                    self.worker_thread.start()
                    # self.worker_thread.wait()
                    
                    loop = QEventLoop()
                    self.worker_thread.finished_signal.connect(loop.quit)

                    timer = QTimer()
                    timer.timeout.connect(lambda: self.periodic_function(current_value, dir_len))
                    timer.start(100)

                    loop.exec_()
                    timer.stop()
                    
                    self.progress_bar.setValue(current_value + 1000 // dir_len)

            self.progress_bar.setValue(1000)
            self.layout.removeWidget(self.progress_bar)
                    

    def update_status(self, message):
        self.status_label.setText(message)

    def update_ui(self):
        self.auto_option = self.dropdown.currentText()
        if self.auto_option == "Bulk Delete":
            self.label.setVisible(False)
            self.textbox.setVisible(False)
            self.cat_dropdown.setVisible(False)
            self.tag_dropdown.setVisible(False)
            self.selected_tags_label.setVisible(False)
            self.price_label.setVisible(False)
            self.price_dropdown.setVisible(False)
            self.pro_price_label.setVisible(False)
            self.pro_price_dropdown.setVisible(False)
            self.add_label.setVisible(False)
            self.add_textbox.setVisible(False)
            self.folder_drop_widget.setDisabled(True)
            self.folder_drop_widget.folder_label.setText("Folder selection not required for Bulk Delete.")
            self.checkbox.setVisible(False)
            self.hcheckbox.setVisible(True)
        elif self.auto_option == 'Edit Model':
            self.label.setVisible(False)
            self.textbox.setVisible(False)
            self.cat_dropdown.setVisible(False)
            self.tag_dropdown.setVisible(True)
            self.selected_tags_label.setVisible(True)
            self.price_label.setVisible(True)
            self.price_dropdown.setVisible(True)
            self.pro_price_label.setVisible(True)
            self.pro_price_dropdown.setVisible(True)
            self.add_label.setVisible(True)
            self.add_textbox.setVisible(True)
            self.folder_drop_widget.setDisabled(False)
            self.folder_drop_widget.folder_label.setText("Drop a folder here")
            self.checkbox.setVisible(True)
            self.hcheckbox.setVisible(True)
        else:
            self.label.setVisible(True)
            self.textbox.setVisible(True)
            self.cat_dropdown.setVisible(True)
            self.tag_dropdown.setVisible(True)
            self.selected_tags_label.setVisible(True)
            self.price_label.setVisible(True)
            self.price_dropdown.setVisible(True)
            self.pro_price_label.setVisible(True)
            self.pro_price_dropdown.setVisible(True)
            self.add_label.setVisible(True)
            self.add_textbox.setVisible(True)
            self.folder_drop_widget.setDisabled(False)
            self.folder_drop_widget.folder_label.setText("Drop a folder here")
            self.checkbox.setVisible(True)
            self.hcheckbox.setVisible(True)
        
    def update_category(self):
        self.cat_option = self.cat_dropdown.currentText()

    def on_checkbox_toggled(self, state):
        if state == 2: 
            self.submit_for_rev = True
        else:  # 0 means Unchecked
            self.submit_for_rev = False

    def headless_toggle(self, state):
        if state == 2: 
            self.headless = True
        else:  # 0 means Unchecked
            self.headless = False 
                        


def main():
    app = QApplication(sys.argv)
    gui = AutomationGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()