from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.io as pio
import tempfile
import os
from PyQt5.QtCore import QUrl

class ConvergencePlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set up layout
        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        
        # Initialize empty plot
        self.update_plot([])

    def update_plot(self, fitness_data):
        # Create Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=fitness_data, 
            mode='lines+markers', 
            line=dict(color="lightblue"),
            marker=dict(size=6)
        ))
        
        # Set figure background and layout colors
        fig.update_layout(
            title="Convergence Graph",
            xaxis_title="Generation",
            yaxis_title="Fitness (Spearman Correlation)",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="lightblue"),
            xaxis=dict(showgrid=True, gridcolor="lightblue"),
            yaxis=dict(showgrid=True, gridcolor="lightblue")
        )
        
        # Save the plot as an HTML file and load it in the QWebEngineView
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            pio.write_html(fig, file=f.name, auto_open=False)
            temp_file_path = os.path.abspath(f.name)
            self.web_view.setUrl(QUrl.fromLocalFile(temp_file_path))

            # Optionally, delete the temporary HTML file after loading
            def cleanup():
                if os.path.exists(f.name):
                    os.remove(f.name)
            
            # Using loadFinished to ensure that the content has been fully loaded before cleanup
            self.web_view.page().loadFinished.connect(lambda: cleanup())
