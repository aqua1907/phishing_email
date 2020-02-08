import utils.config as cfg
import re
import json
import os


def read_pers_info():
    smtp_server = ""
    email = ""
    password = ""
    refresh_rate = ""
    if os.path.exists(cfg.pers_inf_json):
        with open(cfg.pers_inf_json) as json_file:
            pers_inf = json.load(json_file)
            smtp_server = pers_inf["smtp_server"]
            email = pers_inf["email"]
            password = pers_inf["password"]
            refresh_rate = pers_inf["refresh_rate"]

        json_file.close()

    return smtp_server, email, password, refresh_rate


def create_pers_info(widget):
    """
    Create a JSON file from the dictionary "pers_inf"
    """
    pers_inf = {"smtp_server": widget.lineEdit.text(),
                "email": widget.lineEdit_2.text(),
                "password": widget.lineEdit_3.text(),
                "refresh_rate": widget.lineEdit_4.text()
                }

    with open(cfg.pers_inf_json, 'w') as json_file:
        json.dump(pers_inf, json_file)
    json_file.close()


def check_email(connection, notification, json_file):
    """
    :param connection: it is a imbox connection
    :param notification: get toaster object to call notification
    :param json_file: get a json file with all data feed
    :return: pop up windows notification
    """
    # Two lists for print malicious ips and urls that email has
    malicious_ips = []
    malicious_urls = []
    attachment = ''

    # Select unseen emails
    unread_inbox_messages = connection.messages(unread=True)
    # Looping all over unseen emails
    for uid, message in unread_inbox_messages:
        # Get user FROM email
        from_email = message.sent_from[0]['email']

        # Get name of attachment in the email
        if message.attachments:
            attachment = message.attachments[0]['filename']

        # Get email message
        body = message.body['plain']
        # ips = re.findall(cfg.ip_regex, body[0])
        # Find all urls from email message
        urls = re.findall(cfg.url_regex, body[0])

        # if ips:
        #     malicious_ips = set(ips).intersection(json_file['phishing_ips'])

        # Check if received email consists
        if urls:
            urls = [url.strip().replace("<", r"").replace(">", r"") for url in urls]
            malicious_urls = set(urls).intersection(json_file['phishing_urls'])

        # If url is malicious and email consists attachment print alert message
        if malicious_urls and attachment is not None:
            notification.show_toast("Threat Alert", f"Email from {from_email} has a malicious link and an attachment",
                                    duration=10)
        # If url is malicious print alert message
        elif malicious_urls:
            notification.show_toast("Threat Alert", f"Email from {from_email} has malicious link",
                                    duration=10)
        # If email consists attachment print alert message
        elif attachment is not None:
            notification.show_toast("Threat Alert", f"Alert! You received email from {from_email} with an attachment",
                                    duration=10)






