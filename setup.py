import json

from pathlib import Path

# TODO(zndf): Fix wonky file I/O operations, they often fail because the file
#             have not yet been created or because the file content is empty

def load_config():
    with open("config.json", "r") as config_file:
        try:
            config = json.load(config_file)
        except json.decoder.JSONDecodeError:
            config = {}

        return config

def save_to_config(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

def first_run():
    try:
        first_run = load_config().get("first_run")
    except FileNotFoundError:
        first_run = True

    if first_run is True or first_run is None:
        return True
    return False

def get_details():
    _email = str(input("Siakad Email : "))
    _password = str(input("Siakad Password : "))
    _browser = str(input("Browser : "))
    return _email, _password, _browser

def set_details():
    _email, _password, _browser = get_details()

    try:
        config = load_config()
    except json.decoder.JSONDecodeError:
        config = {}

    config["first_run"] = False
    config["email"] = _email
    config["password"] = _password
    config["browser"] = _browser

    save_to_config(config)

if __name__ == '__main__':
    if not first_run():
        print("This is not your first run, are you sure to reconfigure?")
        input("Press enter to continue or Ctrl+C to quit")

    Path("config.json").touch(exist_ok=True)

    set_details()
