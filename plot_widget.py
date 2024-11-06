from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ConvergencePlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(facecolor='black')  # Set the figure background to black
        self.ax = fig.add_subplot(111)
        self.ax.set_title("Convergence Graph", color='lightblue')  # Title color
        self.ax.set_xlabel("Generation", color='lightblue')  # X-axis label color
        self.ax.set_ylabel("Fitness (Spearman Correlation)", color='lightblue')  # Y-axis label color
        self.ax.tick_params(axis='x', colors='lightblue')  # X-axis ticks color
        self.ax.tick_params(axis='y', colors='lightblue')  # Y-axis ticks color
        self.ax.set_facecolor('black')  # Background color of the plot area
        super().__init__(fig)
        self.setParent(parent)
    
    def update_plot(self, fitness_data):
        self.ax.clear()  # Clear previous plot
        self.ax.plot(fitness_data, color="lightblue")  # Line color
        self.ax.set_title("Convergence Graph", color='lightblue')  # Title color
        self.ax.set_xlabel("Generation", color='lightblue')  # X-axis label color
        self.ax.set_ylabel("Fitness (Spearman Correlation)", color='lightblue')  # Y-axis label color
        self.ax.tick_params(axis='x', colors='lightblue')  # X-axis ticks color
        self.ax.tick_params(axis='y', colors='lightblue')  # Y-axis ticks color
        self.ax.set_facecolor('black')  # Background color of the plot area
        
        # Add grid
        self.ax.grid(color='lightblue', linestyle='--', linewidth=0.5)  # Customize grid color and style
        
        self.draw()  # Redraw the canvas