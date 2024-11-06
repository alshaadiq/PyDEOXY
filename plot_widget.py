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

        # Generate x-values starting from 1
        x_values = list(range(1, len(fitness_data) + 1))

        # Add main line trace for fitness data
        fig.add_trace(go.Scatter(
            x=x_values,
            y=fitness_data, 
            mode='lines+markers', 
            line=dict(color="orange"),
            marker=dict(size=6),
            name="Convergence Line"
        ))

        # Highlight the maximum y-value with a special marker
        if fitness_data:  # Ensure there is data to process
            max_y = max(fitness_data)
            max_index = fitness_data.index(max_y)
            # Add a marker for the maximum point
            fig.add_trace(go.Scatter(
                x=[max_index],
                y=[max_y],
                mode='markers+text',
                marker=dict(color="red", size=10),
                text=[f"Max: {max_y:.2f}"],  # Display max y-value as text
                textposition="top center",
                name="Maximum Fitness"
            ))
        
        # Set figure background and layout colors
        fig.update_layout(
            title="Convergence Graph",
            xaxis_title="Generation",
            yaxis_title="Fitness (Spearman Correlation)",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="lightblue"),
            xaxis=dict(showgrid=True, gridcolor="lightblue", range=[1, len(fitness_data)]),
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
