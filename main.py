import json
import time
from utils.utils import *
from imbox import Imbox
from win10toast import ToastNotifier

if __name__ == "__main__":
    # Create toaster object for poping up windows notifications
    toaster = ToastNotifier()
    # Load all feed data from json file
    mlui = json.load(open(r"data/malicious_urls_ips.json"))

    # Checking unseen emails until close the program
    while True:
        # Initialise object using "with" statement
        with Imbox(cfg.SMTP_SERVER,   # imap server
                   username=cfg.EMAIL,
                   password=cfg.PWD,
                   ssl=True,
                   ssl_context=None,
                   starttls=False) as imbox:

            # Run function that checks email on threat
            check_email(imbox, toaster, mlui)
            # It is something like refresh rate
            time.sleep(5)

