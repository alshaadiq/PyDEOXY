import sys
from PyQt5.QtWidgets import QApplication
from gui import GeneticAlgorithmGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GeneticAlgorithmGUI()
    gui.resize(1200, 800)
    gui.show()
    sys.exit(app.exec_())