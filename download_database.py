import requests
import json
import gzip
import shutil
import utils.config as cfg

# Get data from phishtank.com
phishtank_json_gz = requests.get("http://data.phishtank.com/data/online-valid.json.gz").content

# Get txt file from openfish.com
openfish_txt = requests.get("https://openphish.com/feed.txt").content
# Decode txt file from bytes to UTF-8 and split by each line to create a list
openfish_list = openfish_txt.decode('UTF-8').splitlines()

# Get txt file from normshield.com
normshield_txt = requests.get("https://services.normshield.com/domain/fraudulent/text/").content
# Decode txt file from bytes to UTF-8 and split by each line to create a list,
# and slice 9 lines because of comments in txt file
normshield_list = normshield_txt.decode("UTF-8").splitlines()[9:]
# Normalize url to 'http:// url/'
normshield_list = ['http://' + url + '/' for url in normshield_list]

# Write to the disk .gz archive
with open(cfg.phishtank_json_gz_path, 'wb') as fileObject:
    fileObject.write(phishtank_json_gz)
fileObject.close()

# Open .gz archive and write data to the json file
with gzip.open(cfg.phishtank_json_gz_path, 'rb') as f_in:
    with open(cfg.phishtank_json_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
f_out.close()
f_in.close()

# Load json file with data
phishtank_json = json.load(open(cfg.phishtank_json_path))
# Initialise empty lists for urls and ips
phishing_urls = []
phishing_ips = []

# Append urls from openfish and normshield to the phishing_urls list
for feed in [openfish_list, normshield_list]:
    for url in feed:
        phishing_urls.append(url)

# Append urls from phishtank by parsing json file
for phish_dict in phishtank_json:
    phishing_urls.append(phish_dict.get("url", None))
    # Get "details" key for find malicious ips
    details = phish_dict.get("details", [])
    for detail in details:
        # Append ips to phishing_ips
        phishing_ips.append(detail.get("ip_address"))

# Create new json files that saves malicious ips and urls
# From openfish, normshield and phishtank resources
with open(cfg.phishing_data_feed, "w") as fileObject:
    fileObject.write(json.dumps({
        "phishing_urls": phishing_urls,
        "phishing_ips": phishing_ips
    }))
fileObject.close()
