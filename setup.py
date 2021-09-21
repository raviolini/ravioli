import json
from selenium import webdriver
from pathlib import Path
from halo import Halo
from colorama import Fore
# TODO(zndf): Fix wonky file I/O operations, they often fail because the file
#             have not yet been created or because the file content is empty
#fixed (seto)


def create_defaultConfig():
    default_data ={
        "first_run" : True,
        "email" : "Email",
        "password" : "Password",
        "browser" : ""
        }    
    json_object = json.dumps(default_data)

    with open("config.json", "w") as file:
        file.write(json_object)

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

def message_info(message):
    Message = Fore.YELLOW + "[INFO] : {_message}".format(_message=message)
    print(Message)

def first_run():
    try:
        first_run = load_config().get("first_run")
    except FileNotFoundError:
        message_info("no config file found")

        create_file_info = Halo(text = "Creating default config file", spinner='dots')
        create_file_info.start()

        create_defaultConfig()
        
        create_file_info.succeed()

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

@Halo(text=Fore.YELLOW + "[INFO] Downloading & installing webdriver \n", spinner="dots")
def setup_webdriver():
    message_info("this feature is under construction")
    browser = load_config().get('browser').lower()

    if browser == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager
        #driver = 
        webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == "chrome":
        from webdriver_manager.chrome import ChromeDriverManager
        #driver = 
        webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "edge":
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        #driver = 
        webdriver.Edge(EdgeChromiumDriverManager().install())


if __name__ == '__main__':
    if not first_run():
        message_info("This is not your first run, are you sure to reconfigure?")
        input("Press enter to continue or Ctrl+C to quit ")

    Path("config.json").touch(exist_ok=True)

    set_details()
