import json

def load_config():
    with open("config.json", "r+") as config:
        return json.load(config)

def first_run():
    state = load_config().get('state')
    if state == 1:
        return True
    else:
        return False

def get_account_details():
    _email = str(input("Siakad Email : "))
    _password = str(input("Siakad Password : "))
    return _email, _password

def set_account_details():
    account_details = get_account_details()
    _email = account_details[0]
    _pass = account_details[1]
    _new_state = 2

    config = load_config()
    config['state'] = _new_state
    config["email"] = _email
    config["password"] = _pass

    save_to_config(config)

def save_to_config(config:dict):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)
    

if __name__ == '__main__':
    print("first run? : ", first_run())
    set_account_details()
