from gui import WeldSeamAnalysisGUI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeldSeamAnalysisGUI()
    window.show()
    sys.exit(app.exec_())