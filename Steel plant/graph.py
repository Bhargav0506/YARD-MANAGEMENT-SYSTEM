import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pymongo
import datetime

class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphs")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItem("Select Graph")
        self.graph_type_combo.addItem("Quantity Graph")
        self.graph_type_combo.addItem("Time Graph")
        self.graph_type_combo.addItem("Bin Graph")
        layout.addWidget(self.graph_type_combo)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.graph_type_combo.currentIndexChanged.connect(self.display_graph)

        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client["INTERNSHIP"]
        self.collection = self.db["YardManagementSystem"]

    def retrieve_data(self):
        data = list(self.collection.find({}, {"item": 1, "quantity": 1, "timestamp": 1, "qr_code_result": 1, "_id": 0}))
        return data

    def show_quantity_graph(self):
        print("Displaying quantity graph...")
        data = self.retrieve_data()
        print("Data retrieved:", data)
        items = []
        quantities = []

        for doc in data:
            items.append(doc["item"])
            quantities.append(int(doc["quantity"]))

        print("Items:", items)
        print("Quantities:", quantities)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(items, quantities)
        ax.set_xlabel('Items')
        ax.set_ylabel('Quantity')
        ax.set_title('Quantity Graph (in tonnes)')
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

    def show_time_graph(self):
        print("Displaying time graph...")
        data = self.retrieve_data()
        print("Data retrieved:", data)
        quantities = []
        timestamps = []

        for doc in data:
            quantities.append(int(doc["quantity"]))
            datetime_obj = datetime.datetime.strptime(doc["timestamp"], "%Y-%m-%d %H:%M:%S")
            date_only = datetime_obj.date()
            date_string = date_only.strftime("%Y-%m-%d")
            timestamps.append(date_string)

        sorted_data = sorted(zip(timestamps, quantities))
        timestamps, quantities = zip(*sorted_data)

        print("Quantities:", quantities)
        print("Timestamps:", timestamps)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(timestamps, quantities)
        ax.set_xlabel('Time')
        ax.set_ylabel('Quantity')
        ax.set_title('Time Graph (in tonnes)')
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

    def show_bin_graph(self):
        print("Displaying bin graph...")
        data = self.retrieve_data()
        print("Data retrieved:", data)
        bins = []
        quantities = []

        for doc in data:
            bins.append(doc["qr_code_result"])
            quantities.append(int(doc["quantity"]))

        print("Bins:", bins)
        print("Quantities:", quantities)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(bins, quantities)
        ax.set_xlabel('Bin')
        ax.set_ylabel('Quantity')
        ax.set_title('Bin Quantity Graph (in tonnes)')
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

    def display_graph(self, index):
        if index == 1:
            self.show_quantity_graph()
        elif index == 2:
            self.show_time_graph()
        elif index == 3:
            self.show_bin_graph()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GraphWindow()
    main_window.show()
    sys.exit(app.exec_())
