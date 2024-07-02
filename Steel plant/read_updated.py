import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, \
    QSizePolicy, QScrollArea, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pymongo import MongoClient

class ReadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Read Data from MongoDB")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout(self)
        self.collection_combo = QComboBox(self)
        self.collection_combo.addItem("Select DB")
        self.collection_combo.addItem("YardManagementSystem")
        self.collection_combo.addItem("Products")
        layout.addWidget(self.collection_combo)
        
        self.collection_combo.currentIndexChanged.connect(self.display_data)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        self.table = QTableWidget(self)
        self.scroll_area.setWidget(self.table)
        
        self.mongo_client = MongoClient('mongodb://localhost:27017/')
    
    def display_data(self):
        try:
            self.table.clear()
            collection_name = self.collection_combo.currentText()
            db = self.mongo_client['INTERNSHIP']
            collection = db[collection_name]
            data = list(collection.find())
            if collection_name == "YardManagementSystem":
                headers = ["_id", "Emp Name", "Emp ID", "Item", "Quantity", "Bin Number", "Latitude", "Longitude", "Timestamp"]
                self.populate_table(data, headers)
            elif collection_name == "Products":
                self.populate_products_table(data)
            print("Data:", data)
        except Exception as e:
            print("An error occurred:", e)
    
    def populate_table(self, data, headers):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.table.setFixedHeight(750)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry.get('_id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(entry.get('emp name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(entry.get('emp id', '')))
            self.table.setItem(row, 3, QTableWidgetItem(entry.get('item', '')))
            self.table.setItem(row, 4, QTableWidgetItem(entry.get('quantity', '')))
            self.table.setItem(row, 5, QTableWidgetItem(entry.get('qr_code_result', '')))
            self.table.setItem(row, 6, QTableWidgetItem(str(entry.get('latitude', ''))))
            self.table.setItem(row, 7, QTableWidgetItem(str(entry.get('longitude', ''))))
            self.table.setItem(row, 8, QTableWidgetItem(str(entry.get('timestamp', ''))))
        
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
    
    def populate_products_table(self, data):
        try:
            headers = ["_id", "Item"]
            bins = sorted(set([key for entry in data for key in entry.keys() if key.startswith("BIN")]))
            headers.extend(bins)
            
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(data))
            
            font = QFont()
            font.setBold(True)
            self.table.horizontalHeader().setFont(font)
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
            self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.table.setFixedHeight(750)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            
            for row, entry in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(str(entry.get('_id', ''))))
                self.table.setItem(row, 1, QTableWidgetItem(entry.get('item', '')))
                for i, bin_key in enumerate(bins, start=2):
                    bin_data = entry.get(bin_key, '')
                    self.table.setItem(row, i, QTableWidgetItem(str(bin_data)))
            
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setStretchLastSection(True)
            print("Data:", data)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    read_window = ReadWindow()
    read_window.show()
    sys.exit(app.exec_())
