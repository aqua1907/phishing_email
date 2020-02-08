from PyQt5.QtWidgets import QApplication
import sys
from ui.widget import Widget



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
