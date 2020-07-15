# Application for spam detection
The desktop application that checks your incoming e-mails whether it is spam or not.

A simple TensorFlow sequence model with ```Conv1D``` and ```MaxPooling1D``` layers and pre-trained Embedding matrix, 
namely 100-dimensional ```word2vec``` gives 96% accuracy. However, this model has high variance because of the lack of the given data.

## Modules
As a UI I am using ```PyQt5``` module:

![IMG](https://github.com/aqua1907/phishing_email/blob/master/images/Annotation%202020-07-15%20162424.png)

```Imbox``` — Python library for reading IMAP mailboxes and converting email content to machine readable data. Very convenient 
module for grabbing e-mails and store data in dictionary format.

```win10toast``` — Python library for displaying Windows10 Toast Notifications.

![IMG](https://github.com/aqua1907/phishing_email/blob/master/images/Annotation%202020-07-15%20155458.png)

## Usage
To start the application execute ```main.py```.

According to screenshot of UI:

- IMAP Server — provide your IMAP server of email and you need to enable IMAP protocol in your email box settings
- Email — your username.email_box.domain
- Password — your password to your email box. Several email services can provide you a special key/password for IMAP protocol
- Refresh rate — in minutes, fill the blank with your number to check your emails every x minutes

Every x minutes app check for a new email message. If you have an incoming email, TensorFlow model will predict if it malicious email or not
and then Windows notification will pop up.

### Requirements
```
pyqt5~=5.15.0
imbox~=0.9.8
win10toast~=0.9
tensorflow~=2.2.0
```
