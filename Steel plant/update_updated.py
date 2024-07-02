import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from pymongo import MongoClient
from bson import ObjectId

class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data in MongoDB")
        self.setGeometry(100, 100, 400, 400)
        
        self.layout = QVBoxLayout(self)
        
        self.collection_combo = QComboBox(self)
        self.collection_combo.addItem("Select DB")
        self.collection_combo.addItem("YardManagementSystem")
        self.collection_combo.addItem("Products")
        self.layout.addWidget(self.collection_combo)
        
        self.collection_combo.currentIndexChanged.connect(self.show_fields)
        
        self.id_label = QLabel("Enter _id (without ObjectId() wrapper):")
        self.id_input = QLineEdit()
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)
        
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['INTERNSHIP']
        self.collection_ym = self.db['YardManagementSystem']
        self.collection_products = self.db['Products']
        
        self.hide_input_fields()
        
        self.fetch_button = QPushButton("Fetch Details")
        self.fetch_button.clicked.connect(self.fetch_details)
        self.layout.addWidget(self.fetch_button)
        
        self.submit_button = QPushButton("Submit Changes")
        self.submit_button.clicked.connect(self.update_data)
        self.submit_button.setEnabled(False)
        self.layout.addWidget(self.submit_button)
    
    def show_fields(self):
        selected_collection = self.collection_combo.currentText()
        if selected_collection == "Select DB":
            self.hide_input_fields()
            self.submit_button.setEnabled(False)
        elif selected_collection == "YardManagementSystem":
            self.show_ym_fields()
        elif selected_collection == "Products":
            self.show_products_fields()
    
    def hide_input_fields(self):
        for widget in self.findChildren(QLabel):
            widget.hide()
        for widget in self.findChildren(QLineEdit):
            widget.hide()
    
    def show_ym_fields(self):
        self.hide_input_fields()
        self.id_label.setText("Enter _id (without ObjectId() wrapper):")
        self.id_label.show()
        self.id_input.show()
    
    def show_products_fields(self):
        self.hide_input_fields()
        self.id_label.setText("Enter _id (without ObjectId() wrapper):")
        self.id_label.show()
        self.id_input.show()
    
    def fetch_details(self):
        doc_id = self.id_input.text()
        try:
            doc_id = ObjectId(doc_id)
            selected_collection = self.collection_combo.currentText()
            if selected_collection == "YardManagementSystem":
                doc = self.collection_ym.find_one({'_id': doc_id})
            elif selected_collection == "Products":
                doc = self.collection_products.find_one({'_id': doc_id})
            if doc:
                self.populate_input_fields(doc)
                self.submit_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Error", "Document not found.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def populate_input_fields(self, doc):
        self.hide_input_fields()
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)
        for key, value in doc.items():
            label = QLabel(f"{key}:")
            input_field = QLineEdit(str(value))
            self.layout.addWidget(label)
            self.layout.addWidget(input_field)
    
    def update_data(self):
        doc_id = self.id_input.text()
        try:
            doc_id = ObjectId(doc_id)
            selected_collection = self.collection_combo.currentText()
            update_data = {}
            for label, line_edit in zip(self.findChildren(QLabel), self.findChildren(QLineEdit)):
                field_name = label.text().split(':')[0].strip()
                field_value = line_edit.text().strip()
                if field_name != 'Enter _id (without ObjectId() wrapper)' and field_value:
                    update_data[field_name] = field_value
            
            update_data.pop('_id', None)
            
            if selected_collection == "YardManagementSystem":
                update_result = self.collection_ym.update_one({'_id': doc_id}, {'$set': update_data})
            elif selected_collection == "Products":
                update_result = self.collection_products.update_one({'_id': doc_id}, {'$set': update_data})
            
            if update_result.modified_count > 0:
                QMessageBox.information(self, "Update Success", f"{selected_collection} data updated successfully.")
            else:
                QMessageBox.warning(self, "Update Failed", "No changes were made.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_window = UpdateWindow()
    update_window.show()
    sys.exit(app.exec_())
