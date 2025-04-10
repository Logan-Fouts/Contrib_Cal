import json
import urequests

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config
    except:
        print("No config found. Using defaults (if any).")
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print("Config saved.")

def unquote(string):
    """Basic URL decoding"""
    replacements = {
        '%20': ' ',
        '%40': '@',
        '%21': '!',
        '%24': '$',
        '%26': '&'
    }
    for code, char in replacements.items():
        string = string.replace(code, char)
    return string