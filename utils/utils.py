import string
import numpy as np
import utils.config as cfg
import re
import json
import os
from tensorflow.keras.preprocessing import sequence


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


def text_to_wordlist(text):
    # Remove puncuation
    text = text.translate(string.punctuation)

    # Convert words to lower case and split them
    text = text.lower().split()

    # Remove stop words
    # stops = set(stopwords.words("english"))
    # text = [w for w in text if not w in stops and len(w) >= 3]

    text = " ".join(text)
    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text


def check_email(connection, notification, model, tokenizer):
    """
    :param connection: it is a imbox connection
    :param notification: get toaster object to call notification
    :param model: loaded model for prediction spam
    :param tokenizer: process given email text to tokens
    :return: pop up windows notification
    """
    # Empty string for handling attachments
    attachment = None

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
        body = message.body['plain'][0]
        # Check email content using model
        predicted_email = predict_spam(body, model, tokenizer)
        # Find all urls from email message
        urls = re.findall(cfg.url_regex, body)

        # Check if received email consists
        if urls:
            urls = [url.strip().replace("<", r"").replace(">", r"") for url in urls]

        # If email contains urls and attachments print alert message
        if urls and attachment is not None:
            if predicted_email < 0.5:
                notification.show_toast("Threat Alert", "Email from {} contains a link and an attachment. "
                                                        "Not enough email content for prediction a threat".format(from_email),
                                        duration=5)
            else:
                notification.show_toast("Threat Alert", "Email from {} contains a link and an attachment. "
                                                        "Probality of threat is {:.2f}%".format(from_email,
                                                                                                predicted_email * 100),
                                        duration=5)
        # If email contains url print alert message
        elif urls:
            if predicted_email < 0.5:
                notification.show_toast("Threat Alert", "Email from {} contains a link. "
                                                        "Not enough email content for prediction a threat".format(from_email),
                                        duration=5)
            else:
                notification.show_toast("Threat Alert", "Email from {} contains a link. "
                                                        "Probality of threat is {:.2f}%".format(from_email,
                                                                                                predicted_email * 100),
                                        duration=5)
        # If email consists attachment print alert message
        elif attachment is not None:
            if predicted_email < 0.5:
                notification.show_toast("Threat Alert", "Email from {} with an attachment. "
                                                        "Not enough email content for prediction a threat".format(from_email),
                                        duration=5)
            else:
                notification.show_toast("Threat Alert", "Email from {} with an attachment. "
                                                        "Probality of threat is {:.2f}%".format(from_email,
                                                                                                predicted_email * 100),
                                        duration=10)

        else:
            if predicted_email < 0.5:
                notification.show_toast("Threat Alert", "Email from {} is clear.".format(from_email),
                                        duration=5)
            else:
                notification.show_toast("Threat Alert", "Email from {} is potentially a threat. "
                                                        "Probality of threat is {:.2f}%".format(from_email,
                                                                                                predicted_email * 100),
                                        duration=5)


def predict_spam(email_text, model, tokenizer):
    """
    :param email_text: an email that needs to be detected as spam or not
    :param model: loaded model for prediction spam
    :param tokenizer: process given email text to tokens
    :return: probability of detected threat, the value lay between 0 to 1
    """

    processed_text = text_to_wordlist(email_text)
    tokens = tokenizer.texts_to_sequences([processed_text])
    paded_sequences = sequence.pad_sequences(tokens, maxlen=300, padding='post')
    prediction = model.predict(paded_sequences)

    return prediction[0][0]
