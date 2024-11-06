def style_sheet():
    return """
    QWidget {
        background-color: black;
        color: lightblue;
        font-family: 'Arial', sans-serif;
    }
    QPushButton {
        background-color: lightblue;
        color: black;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #e37043; /* Slightly darker on hover */
    }
    QPushButton:pressed {
            background-color: #b65a35; /* Pressed color, slightly darker */
    }
    QLineEdit {
        background-color: #222222;
        color: lightblue;
        border: 1px solid lightblue;
        border-radius: 5px;
        padding: 5px;
    }
    QLabel {
        font-size: 14px;
    }
    QTextEdit {
        background-color: #222222;
        color: lightblue;
        border: 1px solid lightblue;
        border-radius: 5px;
        padding: 5px;
    }
    QTableWidget {
        background-color: #333333; /* Dark background for table */
        color: lightblue; /* Text color */
        border: 1px solid lightblue;
    }
    QSplitter::handle {
        background-color: lightblue;
    }
    """
