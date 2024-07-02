import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import pymongo

class SalesGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Graph")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client["INTERNSHIP"]
        self.sales_collection = self.db["Sales"]

        self.plot_sales_graph()

    def plot_sales_graph(self):
        sales_data = self.sales_collection.find({}, {"customer_name": 1, "item": 1, "quantity": 1, "bin": 1, "timestamp": 1, "_id": 0})
        df = pd.DataFrame(list(sales_data))

        # Ensure the timestamp is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'].apply(lambda x: x['$date'] if isinstance(x, dict) else x))

        # Group by item and sum the quantities
        grouped_data = df.groupby('item')['quantity'].sum()

        # Plot the data
        self.ax.clear()
        grouped_data.plot(kind='bar', ax=self.ax)
        self.ax.set_xlabel('Item')
        self.ax.set_ylabel('Total Quantity Sold')
        self.ax.set_title('Total Sales by Item')
        self.ax.tick_params(axis='x', rotation=45)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sales_graph_window = SalesGraphWindow()
    sales_graph_window.show()
    sys.exit(app.exec_())
