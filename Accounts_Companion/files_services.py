import json
import os

current_path = os.getcwd()
file_config_path = os.path.join(current_path, 'Accounts_Companion', 'configs.json')
base_config = { "vendor-collection": [] }

def check_and_create_config_file():
    if not os.path.exists(file_config_path): 
        with open(file_config_path, 'w') as file:
            json.dump(base_config, file, indent=2)

def read_json():
    check_and_create_config_file()
    
    with open(file_config_path, 'r') as file:
        return json.load(file)

def write_json(data):
    with open(file_config_path, 'w') as file:
        json.dump(data, file, indent=2)
