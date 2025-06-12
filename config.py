import os
from dotenv import load_dotenv

load_dotenv()

USER_DATA_DIR = os.getenv("USER_DATA_DIR")
USER_AGENT = os.getenv("USER_AGENT")
SCROLL_LIMIT = int(os.getenv("SCROLL_LIMIT")) if os.getenv("SCROLL_LIMIT") else None
SCROLL_TIME = int(os.getenv("SCROLL_TIME")) if os.getenv("SCROLL_TIME") else None
WEBSITE_URL = "https://fab.com/portal/listings"
# CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH") or "chromedriver"  # Default to 'chromedriver' if not set

GUI_STYLE = """
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
                letter-spacing: 2px;
                color:black;
            }

            QScrollArea {
                border-radius: 10px;
                padding: 5px;
                background: rgb(100, 100, 100);
            }

            QScrollArea > QWidget > QWidget {
                background-color: transparent; /* Ensures transparency for the scroll area content */
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
                color: white;
                border: 1px double gray;
                border-radius: 5px;
                
                font-family: "Roboto";
                font-size: 16px;
                font-weight: 900;
            }

            QPushButton#a-btn {
                padding: 10px 10px 10px 10px;
                background: #00ff00;
                color: black;
            }
                           
            QPushButton#s-btn {
                min-width: 250px;
                color: white;
                background: #04a199;
            }
                           
            QPushButton#q-btn {
                min-width: 250px;
                background: rgb(250, 40, 40);
            }

            QPushButton#a-btn:disabled {
                color: gray;
                background-color: #d3d3d3;
            }
        """
                # background: rgba(0, 180, 20, 0.8);
                #05B8CC;

DRAG_DROP_AREA_STYLE = """
            QWidget {
                border-radius: 5px;
                border: 1px solid rgba(200, 200, 200, 0.8);
                background-color: rgba(200, 200, 200, 0.25);
                padding: 40px 80px 40px 80px;
            }
        """

PROGRESS_STYLE = """
    QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #05B8CC;
        width: 20px;
    }
"""

TAGS = ['Abandoned', 'Abbey', 'Abdomen', 'Aberdeenshire', 'Abies', 'Ability', 'Abomination', 'Aboriginal', 'Absorber', 'Abstract', 'Acacia', 'Academy', 'Acanthus', 'Accent', 'Accessibility', 'Accessory', 'Accident', 'Accord', 'Accordion', 'Accounting', 'Baby', 'Babylon', 'Babylonian', 'Back', 'Background', 'Backhoe', 'Backlight', 'Backpack', 'Backroom', 'Backup', 'Backwall', 'Backyard', 'Bacon', 'Bacteria', 'Badge', 'Badger', 'Badlands', 'Bag', 'Bagel', 'Baggy', 'Cab', 'Cabbage', 'Cabin', 'Cabinet', 'Cable', 'Cacao', 'Cactus', 'Cad', 'Caddy', 'Caesar', 'Cafe', 'Cafeteria', 'Cage', 'Cairn', 'Cairo', 'Cake', 'Calamari', 'Calavera', 'Calculator', 'Caldera', 'Dace', 'Dachshund', 'Dacia', 'Dacian', 'Dacite', 'Dad', 'Daemon', 'Dagger', 'Daily', 'Dairy', 'Daisy', 'Dakar', 'Dali', 'Dallas', 'Dalmatian', 'Dam', 'Damage', 'Damaged', 'Damascus', 'Damp', 'Eagle', 'Ear', 'Earbuds', 'Early', 'Earphone', 'Earring', 'Earth', 'Earthenware', 'Earthquake', 'East', 'Easter', 'Easteregg', 'Eastern', 'Eat', 'Ebony', 'Echinoderm', 'Echinoid', 'Echo', 'Eclipse', 'Ecology', 'Fable', 'Fabric', 'Fabrication', 'Fabricmaking', 'Facade', 'Face', 'Facial', 'Facility', 'Faction', 'Factory', 'Faded', 'Fail', 'Fair', 'Fairy', 'Fairytale', 'Faith', 'Fake', 'Falchion', 'Falcon', 'Fall', 'Gabbro', 'Gable', 'Gadget', 'Gaea', 'Gaia', 'Gala', 'Galactic', 'Galaxy', 'Galleon', 'Gallery', 'Gallon', 'Galvanized', 'Gambling', 'Gamepad', 'Gameplay', 'Gamer', 'Gameready', 'Gaming', 'Ganesha', 'Gang', 'Habitat', 'Habitation', 'Hack', 'Hacker', 'Hades', 'Hadrosaur', 'Hair', 'Hairband', 'Haircut', 'Hairdresser', 'Hairdressing', 'Hairdryer', 'Hairless', 'Hairpin', 'Hairstyle', 'Hairy', 'Halberd', 'Half', 'Halfpipe', 'Hall', 'Iberian', 'Ice', 'Iceage', 'Icecream', 'Iceland', 'Icelandic', 'Ichnofossil', 'Ichthyology', 'Ichthyosaur', 'Icicle', 'Icing', 'Icon', 'Iconic', 'Iconography', 'Icosahedron', 'Idea', 'Ideal', 'Identity', 'Idle', 'Idol', 'Jackal', 'Jacket', 'Jackolantern', 'Jacuzzi', 'Jade', 'Jagged', 'Jaguar', 'Jail', 'Jakarta', 'Jam', 'January', 'Japan', 'Japanese', 'Japonica', 'Japonicus', 'Jar', 'Java', 'Javanese', 'Javelin', 'Jaw', 'Kabuto', 'Kaiju', 'Kaiser', 'Kalash', 'Kalba', 'Kangaroo', 'Kansas', 'Kanto', 'Kappa', 'Karabiner', 'Karambit', 'Karate', 'Karkala', 'Karma', 'Karst', 'Katana', 'Kathmandu', 'Kawaii', 'Kayak', 'Kazakhstan', 'Label', 'Laboratory', 'Lace', 'Lacquered', 'Ladder', 'Ladieswear', 'Ladle', 'Lady', 'Lagoon', 'Lake', 'Lamancha', 'Lamb', 'Lamp', 'Lamppost', 'Lampshade', 'Lance', 'Lancer', 'Land', 'Landing', 'Landscape', 'Macaw', 'Mace', 'Machete', 'Machine', 'Machinegun', 'Machinery', 'Macro', 'Madagascar', 'Madeira', 'Madness', 'Madrid', 'Mafia', 'Magazine', 'Mage', 'Magic', 'Magical', 'Magma', 'Magnet', 'Magnetic', 'Magnificent', 'Nail', 'Name', 'Nameplate', 'Namforsen', 'Nanite', 'Nano', 'Nanotechnology', 'Nantes', 'Napkin', 'Naples', 'Napoleon', 'Napoleonic', 'Narrow', 'Nation', 'National', 'Native', 'Natural', 'Nature', 'Nautical', 'Nautiloid', 'Oak', 'Oakland', 'Oar', 'Oasis', 'Oat', 'Obelisk', 'Obese', 'Object', 'Objective', 'Oblivion', 'Observation', 'Observatory', 'Observer', 'Obsidian', 'Obstacle', 'Ocarina', 'Occipital', 'Occlusion', 'Occult', 'Ocean', 'Pacific', 'Pack', 'Package', 'Packaging', 'Packet', 'Packing', 'Pad', 'Padded', 'Paddle', 'Pagan', 'Page', 'Pagoda', 'Paid', 'Pail', 'Pain', 'Painkiller', 'Paint', 'Paintball', 'Paintbrush', 'Painted', 'Qatar', 'Qi', 'Qing', 'Quad', 'Quadcopter', 'Quadruped', 'Quantum', 'Quarantine', 'Quarry', 'Quarter', 'Quartz', 'Quartzite', 'Quaternary', 'Quay', 'Quebec', 'Queen', 'Queensland', 'Quern', 'Quest', 'Question', 'Rabbit', 'Raccoon', 'Race', 'Racecar', 'Racer', 'Racetrack', 'Racing', 'Rack', 'Racket', 'Racoon', 'Radar', 'Radial', 'Radiant', 'Radiation', 'Radiator', 'Radimlja', 'Radio', 'Radioactive', 'Radiolaria', 'Radiology', 'Saber', 'Sabertooth', 'Sable', 'Sac', 'Sachet', 'Sack', 'Sacral', 'Sacred', 'Sacrifice', 'Sacrum', 'Sad', 'Saddle', 'Safari', 'Safe', 'Safety', 'Saga', 'Sage', 'Sagittarius', 'Sago', 'Sahara', 'Tab', 'Tabernacle', 'Table', 'Tablecloth', 'Tablet', 'Tabletennis', 'Tabletop', 'Tabouret', 'Tabulate', 'Tac', 'Tackle', 'Taco', 'Tactical', 'Tactile', 'Taekwondo', 'Tag', 'Tahiti', 'Tai', 'Tail', 'Tailor', 'Uae', 'Uav', 'Ube', 'Udim', 'Ufo', 'Uganda', 'Ugly', 'Ukraine', 'Ukulele', 'Ulna', 'Ultimate', 'Ultra', 'Umbrella', 'Unbranded', 'Uncle', 'Unconformity', 'Undead', 'Underground', 'Underpass', 'Underwater', 'Vacation', 'Vaccine', 'Vacuum', 'Vale', 'Valencia', 'Valenciana', 'Valentine', 'Valhalla', 'Valkyrie', 'Valley', 'Vampire', 'Van', 'Vancouver', 'Vandal', 'Vandalism', 'Vangogh', 'Vanilla', 'Vanity', 'Vapor', 'Vaporwave', 'Wacky', 'Wadi', 'Wafer', 'Waffle', 'Wagon', 'Waist', 'Waistcoat', 'Waiter', 'Waiting', 'Waitingroom', 'Waitress', 'Wake', 'Wakizashi', 'Wales', 'Walk', 'Walkcycle', 'Walker', 'Walkietalkie', 'Walkway', 'Wall', 'Xenolith', 'Xian', 'Xray', 'Yacht', 'Yak', 'Yakuza', 'Yamato', 'Yang', 'Yankee', 'Yard', 'Yarn', 'Yayoi', 'Year', 'Yellow', 'Yeti', 'Yin', 'Yoga', 'Yogurt', 'Yokai', 'York', 'Yorkshire', 'Yosemite', 'Young', 'Zaragoza', 'Zealand', 'Zebra', 'Zen', 'Zeppelin', 'Zeus', 'Zhou', 'Zinc', 'Zip', 'Zircon', 'Zodiac', 'Zombie', 'Zone', 'Zoo', 'Zoology', 'Zoom', 'Zoomorphic', 'Zucchini', 'Zurich', 'Zweihander']
PRICES = ["0.0 (USD)", "0.99 (USD)", "1.99 (USD)", "2.99 (USD)", "3.99 (USD)", "4.99 (USD)", "5.99 (USD)", "6.99 (USD)", "7.99 (USD)", "8.99 (USD)", "9.99 (USD)", "10.99 (USD)", "11.99 (USD)", "12.99 (USD)", "13.99 (USD)", "14.99 (USD)", "15.99 (USD)", "16.99 (USD)", "17.99 (USD)", "18.99 (USD)", "19.99 (USD)", "20.99 (USD)", "21.99 (USD)", "22.99 (USD)", "23.99 (USD)", "24.99 (USD)", "25.99 (USD)", "26.99 (USD)", "27.99 (USD)", "28.99 (USD)", "29.99 (USD)", "30.99 (USD)", "31.99 (USD)", "32.99 (USD)", "33.99 (USD)", "34.99 (USD)", "35.99 (USD)", "36.99 (USD)", "37.99 (USD)", "38.99 (USD)", "39.99 (USD)", "40.99 (USD)", "41.99 (USD)", "42.99 (USD)", "43.99 (USD)", "44.99 (USD)", "45.99 (USD)", "46.99 (USD)", "47.99 (USD)", "48.99 (USD)", "49.99 (USD)", "50.99 (USD)", "51.99 (USD)", "52.99 (USD)", "53.99 (USD)", "54.99 (USD)", "55.99 (USD)", "56.99 (USD)", "57.99 (USD)", "58.99 (USD)", "59.99 (USD)", "60.99 (USD)", "61.99 (USD)", "62.99 (USD)", "63.99 (USD)", "64.99 (USD)", "65.99 (USD)", "66.99 (USD)", "67.99 (USD)", "68.99 (USD)", "69.99 (USD)", "70.99 (USD)", "71.99 (USD)", "72.99 (USD)", "73.99 (USD)", "74.99 (USD)", "75.99 (USD)", "76.99 (USD)", "77.99 (USD)", "78.99 (USD)", "79.99 (USD)", "80.99 (USD)", "81.99 (USD)", "82.99 (USD)", "83.99 (USD)", "84.99 (USD)", "85.99 (USD)", "86.99 (USD)", "87.99 (USD)", "88.99 (USD)", "89.99 (USD)", "90.99 (USD)", "91.99 (USD)", "92.99 (USD)", "93.99 (USD)", "94.99 (USD)", "95.99 (USD)", "96.99 (USD)", "97.99 (USD)", "98.99 (USD)", "99.99 (USD)", "104.99 (USD)", "109.99 (USD)", "114.99 (USD)", "119.99 (USD)", "124.99 (USD)", "129.99 (USD)", "134.99 (USD)", "139.99 (USD)", "144.99 (USD)", "149.99 (USD)", "159.99 (USD)", "169.99 (USD)", "179.99 (USD)", "189.99 (USD)", "199.99 (USD)", "209.99 (USD)", "219.99 (USD)", "229.99 (USD)", "239.99 (USD)", "249.99 (USD)", "274.99 (USD)", "299.99 (USD)", "324.99 (USD)", "349.99 (USD)", "374.99 (USD)", "399.99 (USD)", "424.99 (USD)", "449.99 (USD)", "474.99 (USD)", "499.99 (USD)", "599.99 (USD)", "699.99 (USD)", "799.99 (USD)", "899.99 (USD)", "999.99 (USD)", "1099.99 (USD)", "1199.99 (USD)", "1299.99 (USD)", "1399.99 (USD)", "1499.99 (USD)"]
CATEGORIES = ["Select Category", "Buildings & Architecture", "Characters & Creatures", "Clothing & Jewelry", "Electronics & Technology", "Food & Drink", "Furniture & Fixtures", "Nature & Plants", "Scenes", "Tools, Objects & Decor", "Vehicles & Transportation", "Weapons & Combat"]
TEXTURE_CATEGORIES = ["Select Category", "Art & Traditional", "Building & Human-made", "Damage & Grunge", "Fabric & Clothing", "Nature & Terrain", "Organic", "Variety"]