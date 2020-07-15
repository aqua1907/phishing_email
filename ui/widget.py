import time
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from utils.utils import *
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from imbox import Imbox
from win10toast import ToastNotifier
from tensorflow.keras import models
import pickle


class Worker(QObject):

    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.imap_server, self.email, self.password, self.refresh_rate = read_pers_info()
        # Create toaster object for popping up windows notifications
        self.toaster = ToastNotifier()
        # Load deep learning model
        self.model = models.load_model(cfg.spam_detector_path)
        # Load tokenizer
        self.tokenizer = pickle.load(open(cfg.tokenizer_path, 'rb'))

    def start_button(self):
        # Checking unseen emails until close the program
        while True:
            # Initialise object using "with" statement
            with Imbox(self.imap_server,  # imap server
                       username=self.email,
                       password=self.password,
                       ssl=True,
                       ssl_context=None,
                       starttls=False) as imbox:
                # Run function that checks email on threat
                check_email(imbox, self.toaster, self.model, self.tokenizer)
                # It is something like refresh rate
                time.sleep(60 * int(self.refresh_rate))


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        # Load .ui file. In this file described interface via xml
        uic.loadUi(r'ui/gui_interaction.ui', self)
        # Set window title
        self.setWindowTitle("Spam Detection")

        imap_server, email, password, refresh_rate = read_pers_info()
        # # Fill empty blanks with user personal information if json is exists
        self.lineEdit.setText(imap_server)
        self.lineEdit_2.setText(email)
        self.lineEdit_3.setText(password)
        self.lineEdit_4.setText(refresh_rate)

        # Create JSON file when do click on the "Save" button
        self.pushButton_2.clicked.connect(self.save_info)

        # Thread:
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start_button)

        # Start Button action:
        self.pushButton.clicked.connect(self.thread.start)

    def save_info(self):
        """
        The Function that is connected to the "Save" button
        """
        # Call "creat_json" function to create JSON file
        create_pers_info(self)

