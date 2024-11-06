import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QTextEdit, QTableWidget,
    QTableWidgetItem, QSplitter

)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from genetic_algorithm import genetic_algorithm
from plot_widget import ConvergencePlotWidget
from style_sheet import style_sheet

# GUI Class
class GeneticAlgorithmGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(style_sheet())  # Apply the stylesheet
        self.setWindowIcon(QIcon('pydeoxy.png'))

    def initUI(self):
        layout = QHBoxLayout()

        # Left side layout for input parameters and output
        left_layout = QVBoxLayout()

        # File selection for population
        file_layout = QHBoxLayout()
        self.population_file_label = QLabel("Population CSV File:")
        self.population_file_input = QLineEdit()
        self.population_file_input.setReadOnly(True)
        self.population_file_button = QPushButton("Load Population CSV")
        self.population_file_button.clicked.connect(self.load_population_csv)
        file_layout.addWidget(self.population_file_label)
        file_layout.addWidget(self.population_file_input)
        file_layout.addWidget(self.population_file_button)

        # File selection for expert responses
        expert_file_layout = QHBoxLayout()
        self.expert_file_label = QLabel("Expert Response CSV File:")
        self.expert_file_input = QLineEdit()
        self.expert_file_input.setReadOnly(True)
        self.expert_file_button = QPushButton("Load Expert Response CSV")
        self.expert_file_button.clicked.connect(self.load_expert_response_csv)
        expert_file_layout.addWidget(self.expert_file_label)
        expert_file_layout.addWidget(self.expert_file_input)
        expert_file_layout.addWidget(self.expert_file_button)

        # Parameters
        self.num_generations_label = QLabel("Number of Generations:")
        self.num_generations_input = QLineEdit("50")
        self.mutation_rate_label = QLabel("Mutation Rate:")
        self.mutation_rate_input = QLineEdit("0.05")
        self.crossover_rate_label = QLabel("Crossover Rate:")
        self.crossover_rate_input = QLineEdit("0.95")
        self.num_selected_label = QLabel("Number of Selected Responses:")
        self.num_selected_input = QLineEdit("5")

        # Run Button
        self.run_button = QPushButton("Run Genetic Algorithm")
        self.run_button.clicked.connect(self.run_algorithm)

        # Output Display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        # Expert response table
        self.expert_response_table = QTableWidget()
        self.expert_response_table.setColumnCount(1)  # Assuming expert response is a single row
        self.expert_response_table.setHorizontalHeaderLabels(["Expert Responses"])

        # Add widgets to left layout
        left_layout.addLayout(file_layout)
        left_layout.addLayout(expert_file_layout)
        left_layout.addWidget(QLabel("Expert Response Preview:"))
        left_layout.addWidget(self.expert_response_table)  # Add expert response table
        left_layout.addWidget(self.num_generations_label)
        left_layout.addWidget(self.num_generations_input)
        left_layout.addWidget(self.mutation_rate_label)
        left_layout.addWidget(self.mutation_rate_input)
        left_layout.addWidget(self.crossover_rate_label)
        left_layout.addWidget(self.crossover_rate_input)
        left_layout.addWidget(self.num_selected_label)
        left_layout.addWidget(self.num_selected_input)
        left_layout.addWidget(self.run_button)
        left_layout.addWidget(QLabel("Output:"))
        left_layout.addWidget(self.output_display)

        # Create a QWidget for the left layout and set the layout
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # Table for CSV data preview
        self.table_widget = QTableWidget()

        # Convergence plot widget
        self.convergence_plot = ConvergencePlotWidget()

        # Right layout for table and plot
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("CSV Preview:"))
        right_layout.addWidget(self.table_widget)
        right_layout.addWidget(QLabel("Convergence Plot:"))
        right_layout.addWidget(self.convergence_plot)

        # Create a QWidget for the right layout and set the layout
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # Split the layouts horizontally
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)

        # Set main layout
        layout.addWidget(main_splitter)

        # Create a QLabel for the copyright watermark
        self.copyright_label = QLabel("© Muhammad Fajar Prasetyo and Muhammad Usman Alshaadiq")
        self.copyright_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)  # Align to bottom right
        self.copyright_label.setStyleSheet("color: lightblue; font-size: 10px;")  # Smaller font size

        # Add the copyright label below the convergence plot
        right_layout.addWidget(self.copyright_label, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setLayout(layout)
        self.setWindowTitle("PyDEOXY v0.1.0 (BELOM REVISI)")

    def load_population_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Population CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            self.population_file_input.setText(file_name)
            self.population_data = pd.read_csv(file_name)
            print("Population Data Loaded:\n", self.population_data.head())  # Debugging line
            self.output_display.append("Loaded Population CSV file successfully.\n")
            self.update_table_preview()

    def load_expert_response_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Expert Response CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            self.expert_file_input.setText(file_name)
            self.expert_data = pd.read_csv(file_name, header=None)
            print("Expert Data Loaded:\n", self.expert_data)  # Debugging line
            self.expert_response = self.expert_data.iloc[0].tolist()

            # Update expert response table
            self.expert_response_table.setRowCount(1)  # Only one row for expert response
            self.expert_response_table.setColumnCount(len(self.expert_response))  # Set columns to the number of values in expert response
            for j, item in enumerate(self.expert_response):
                self.expert_response_table.setItem(0, j, QTableWidgetItem(str(item)))
            
            self.output_display.append("Loaded Expert Response CSV file successfully.\n")

    def update_table_preview(self):
        if self.population_data is not None and not self.population_data.empty:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(len(self.population_data.columns))
            for i, row in self.population_data.iterrows():
                self.table_widget.insertRow(i)
                for j, item in enumerate(row):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(item)))
            for j in range(len(self.population_data.columns)):
                self.table_widget.resizeColumnToContents(j)  # Adjust column width
            print("Table updated with data:\n", self.population_data.head())
        else:
            print("No population data to display.")

    def run_algorithm(self):
        num_generations = int(self.num_generations_input.text())
        mutation_rate = float(self.mutation_rate_input.text())
        crossover_rate = float(self.crossover_rate_input.text())
        num_selected = int(self.num_selected_input.text())
        
        # Convert the population DataFrame to a list of lists
        population = self.population_data.values.tolist()

        # Run the genetic algorithm
        best_response = genetic_algorithm(population, self.expert_response, num_generations, mutation_rate, num_selected, crossover_rate, self.output_display, self.convergence_plot)
        self.output_display.append(f"Best Response Found: {best_response}\n")