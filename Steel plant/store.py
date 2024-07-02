import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QDateTime, Qt
import cv2
import json
from urllib.request import urlopen
from pymongo import MongoClient

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = QLabel("Result QR code", self)
        self.coordinates_label = QLabel("Live GPS Coordinates:", self)
        self.video_frame = QLabel(self)
        self.emp_name = QLineEdit(self)
        self.emp_id = QLineEdit(self)
        self.item_input = QLineEdit(self)
        self.quantity_input = QLineEdit(self)
        read_qr_button = QPushButton("Read QR Code", self)
        read_qr_button.clicked.connect(self.start_camera)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Emp Name:", self))
        layout.addWidget(self.emp_name)
        layout.addWidget(QLabel("Emp Id:", self))
        layout.addWidget(self.emp_id)
        layout.addWidget(QLabel("Item:", self))
        layout.addWidget(self.item_input)
        layout.addWidget(QLabel("Quantity:", self))
        layout.addWidget(self.quantity_input)
        layout.addWidget(read_qr_button)
        layout.addWidget(self.video_frame)
        layout.addWidget(self.result_label)
        layout.addWidget(self.coordinates_label)

        self.mongo_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongo_client['INTERNSHIP']
        self.collection = self.db['YardManagementSystem']
        self.collection_new = self.db['Products']

        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scan_qr_code)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QR Code Scanner")

    def start_camera(self):
        self.timer.start(int(1000 / 30))

    def scan_qr_code(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (360, 270))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(gray)
            if data:
                latitude, longitude = get_coordinates_from_ip()
                if latitude is not None and longitude is not None:
                    self.coordinates_label.setText(f"Live GPS Coordinates: Latitude {latitude}, Longitude {longitude}")

                emp_name = self.emp_name.text()
                emp_id = self.emp_id.text()
                item_text = self.item_input.text()
                quantity_text = self.quantity_input.text()
                timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
                data_to_insert = {
                    'emp name': emp_name,
                    'emp id': emp_id,
                    'item': item_text,
                    'quantity': quantity_text,
                    'qr_code_result': data,
                    'latitude': latitude,
                    'longitude': longitude,
                    'timestamp': timestamp
                }
                self.collection.insert_one(data_to_insert)
                self.update_new_collection(item_text, data, quantity_text)

                self.timer.stop()
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.video_frame.setPixmap(pixmap)
                self.video_frame.setAlignment(Qt.AlignCenter)

    def closeEvent(self, event):
        self.timer.stop()
        self.camera.release()
        cv2.destroyAllWindows()
        super().closeEvent(event)

    def update_new_collection(self, item, bin_text, quantity_text):
        doc = self.collection_new.find_one({'item': item})
        if doc:
            updated_quantity = int(doc.get(bin_text, 0)) + int(quantity_text)
            query = {'$set': {bin_text: str(updated_quantity)}}
            self.collection_new.update_one({'_id': doc['_id']}, query)
        else:
            document = {'item': item, bin_text: quantity_text}
            self.collection_new.insert_one(document)

def get_coordinates_from_ip():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    coordinates_str = data.get('loc', '').split(',')
    if len(coordinates_str) == 2:
        return float(coordinates_str[0]), float(coordinates_str[1])
    return None, None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
