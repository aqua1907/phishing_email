from pathlib import Path

# Path to phishtank data archive .gz
phishtank_json_gz_path = Path(r"data/phishtank.json.gz")
# PAth to phishtank data json file
phishtank_json_path = Path(r"data/phishtank.json")
# Path to all save data json file
phishing_data_feed = Path(r"data/malicious_urls_ips.json")

# Put here smtp server of mail service. Example: "imap.gmail.com"
SMTP_SERVER = ""
# Your email. Example: username@mail.com
EMAIL = ""
# Your password to your mail box
PWD = ""

ip_regex = "\\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\b"

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
