from PyQt5.QtWidgets import QApplication
import sys
from ui.widget import Widget


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
