import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QHBoxLayout
from pymongo import MongoClient
from bson import ObjectId

class DeleteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Data from MongoDB")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout(self)
        hbox = QHBoxLayout()
        
        self.id_label = QLabel("Enter _id:")
        self.id_input = QLineEdit()
        
        hbox.addWidget(self.id_label)
        hbox.addWidget(self.id_input)
        layout.addLayout(hbox)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_data)
        layout.addWidget(self.delete_button)
    
    def delete_data(self):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['INTERNSHIP']
            collection = db['YardManagementSystem']
            
            doc_id = self.id_input.text()
            if not doc_id:
                QMessageBox.warning(self, "Input Error", "Please enter a valid _id.")
                return
            
            doc_id = ObjectId(doc_id)
            delete_result = collection.delete_one({'_id': doc_id})
            print("Deleting data...")
            print("Delete result:", delete_result.raw_result)
            
            if delete_result.deleted_count > 0:
                QMessageBox.information(self, "Delete Success", "Record deleted successfully.")
            else:
                QMessageBox.warning(self, "Delete Failed", "No record found with the provided _id.")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    delete_window = DeleteWindow()
    delete_window.show()
    sys.exit(app.exec_())
