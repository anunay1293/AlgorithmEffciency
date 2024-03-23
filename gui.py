import sys
import random
import time
import PyQt5
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QTextEdit, QLabel, QFrame, QInputDialog, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from main import all_algorithms 

class SortingApp(QMainWindow):
    def __init__(self, algorithms):
        super().__init__()
        self.algorithms = algorithms
        self.selected_algorithms = []
        self.selectAllState = True
        self.checkboxes = {}
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Algorithms Efficiency Analyzer Tool")
        self.setGeometry(100, 100, 600, 800)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)

        # Set the application's background color to blue, text to white, and text boxes to grey.
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(92, 172, 238))  # A shade of blue for the background
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White for the text
        palette.setColor(QPalette.Base, QColor(169, 169, 169))  # Grey for the text boxes
        self.setPalette(palette)
        
        self.textBox = QTextEdit()
        self.mainLayout.addWidget(QLabel("Enter list of numbers:"))
        self.mainLayout.addWidget(self.textBox)

        self.buttonsLayout = QHBoxLayout()

        # Generate Random Numbers Button
        self.generateRandomButton = QPushButton("Generate Random Numbers")
        self.generateRandomButton.clicked.connect(self.generateRandomNumbers)
        self.buttonsLayout.addWidget(self.generateRandomButton)

        # Select All Button
        self.selectAllButton = QPushButton("Select All")
        self.selectAllButton.clicked.connect(self.toggleSelectAll)
        self.buttonsLayout.addWidget(self.selectAllButton)

        self.mainLayout.addLayout(self.buttonsLayout)

        self.checkboxFrame = QFrame()
        self.checkboxLayout = QVBoxLayout(self.checkboxFrame)
        for algo in self.algorithms:
            checkBox = QCheckBox(algo['name'])
            checkBox.stateChanged.connect(self.updateSelectedAlgorithms)
            self.checkboxLayout.addWidget(checkBox)
            self.checkboxes[algo['name']] = checkBox  # Store the checkbox in the dictionary
        self.mainLayout.addWidget(self.checkboxFrame)

        self.runButton = QPushButton("Run Selected")
        self.runButton.clicked.connect(self.runSelectedAlgorithms)
        self.mainLayout.addWidget(self.runButton)

        self.logBox = QTextEdit()
        self.logBox.setReadOnly(True)
        self.mainLayout.addWidget(self.logBox)

    def updateSelectedAlgorithms(self):
        self.selected_algorithms = [algo for algo in self.algorithms if self.checkboxes[algo['name']].isChecked()]

    def toggleSelectAll(self):
        for checkBox in self.checkboxes.values():
            checkBox.setChecked(self.selectAllState)
        self.selectAllState = not self.selectAllState
        self.selectAllButton.setText("Deselect All" if not self.selectAllState else "Select All")

    def generateRandomNumbers(self):
        numbers = [str(random.randint(1, 100)) for _ in range(15000)]
        self.textBox.setText(", ".join(numbers))

    def runSelectedAlgorithms(self):
        self.logBox.clear()  # Clear the log box for new logs
        numbers_str = self.textBox.toPlainText().strip()
        if not numbers_str:
            self.logBox.append("No numbers entered. Please enter a list of numbers separated by spaces or commas.")
            return

        try:
            numbers_list = [int(item.strip()) for item in numbers_str.replace(',', ' ').split()]
        except ValueError as e:
            self.logBox.append(f"Error: Invalid number format. Please enter numbers separated by spaces or commas.")
            return

        algorithms = []
        times = []

        for algo in self.selected_algorithms:
            if algo['name'] == 'Quick Select Sort':
                k, ok = QInputDialog.getInt(self, "Enter k value", "Please enter the value of k:", min=1, max=len(numbers_list), step=1)
                if not ok or k < 1 or k > len(numbers_list):
                    QMessageBox.warning(self, "Invalid k value", "Please enter a valid value of k within the count of numbers you have entered.")
                    return

            start_time = time.time()
            if algo['name'] != 'Quick Select Sort':
                sorted_array = algo['function'](numbers_list.copy())
                self.logBox.append(f"{algo['name']} result: {sorted_array}\n")
            else:
                quick_select_result = algo['function'](numbers_list.copy(), 0, len(numbers_list) - 1, k-1)  # Adjust k to zero-based
                # index
                quick_select_kth_element = quick_select_result[0]
                quick_select_median = quick_select_result[1]
                self.logBox.append(f"{algo['name']} results:")
                self.logBox.append(f"While k={k},  the k-th smallest element "
                                   f"is: {quick_select_kth_element}")
                self.logBox.append(f"The median of the sorted list is "
                                   f"{quick_select_median} ")

            quick_select_kth_element = None
            quick_select_median = None

            end_time = time.time()
            algorithms.append(algo['name'])
            times.append(end_time - start_time)

        if algorithms and times:
            self.plotResults(algorithms, times)

    def plotResults(self, algorithms, times):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 8))
        fig.patch.set_facecolor("#ADD8E6")

        # Set the color palette
        palette = list(reversed(sns.color_palette("seismic", len(algorithms) + 1).as_hex()))[1:]

        ax2.set_facecolor("#ADD8E6")
        ax2.plot(algorithms, times, marker='o', color='orange', label='Line Chart')
        ax2.set_ylim(0, max(times) * 1.1)  # Match y limit with bar chart
        ax2.set_ylabel('Execution Time (seconds)')
        ax2.set_title('Sorting Algorithm Efficiency (Line Chart)')
        ax2.legend()
        ax2.set_xticks(range(len(algorithms)))
        ax2.set_xticklabels(algorithms, rotation=45, ha="right")

        def animate(i, times, palette, ax1, algorithms):
            ax1.clear()
            
            # Scale the current values based on the frame
            scaled_times = [t * i / 50 for t in times]
            
            # Bar chart
            ax1.set_facecolor("#ADD8E6")
            ax1.bar(algorithms, scaled_times, width=0.4, color=palette)
            ax1.set_ylim(0, max(times) * 1.1)  # Set y limit to a bit more than max time for visual appeal
            ax1.set_ylabel('Execution Time (seconds)')
            ax1.set_title("Algorithms Efficiency", color=("blue"))
            ax1.set_xticks(range(len(algorithms)))
            ax1.set_xticklabels(algorithms, rotation=45, ha="right")

            fig.tight_layout()

        ani = FuncAnimation(fig, animate, fargs=(times, palette, ax1, algorithms), interval=50, frames=50, repeat=False)

        self._ani = ani

        plt.show()
        
    def run(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortingApp(all_algorithms)
    window.run()
    sys.exit(app.exec_())