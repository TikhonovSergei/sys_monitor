import sys
from PyQt5.QtWidgets import QApplication
from src.monitors import SystemMonitor


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SystemMonitor()
    sys.exit(app.exec_())