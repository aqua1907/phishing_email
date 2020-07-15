from pathlib import Path

# Path to model
spam_detector_path = Path(r'model/spam_detector.h5')

# Path to tokenizer
tokenizer_path = Path(r'model/tokenizer.pickle')

# Path to user personal information
pers_inf_json = Path(r"data/personal_information.json")

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
