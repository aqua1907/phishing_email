import utils.config as cfg
import re


# def get_from(from_email):
#     """
#     :param from_email: string which has the form : "Name username@mail.com"
#     :return: email as username@mail.com
#     """
#     processed_from_email = from_email.split(" ")[-1].replace("<", r"").replace(">", r"")
#
#     return processed_from_email


def check_email(connection, notification, json_file):
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






