import json
import os

def save_config(com_port, baud_rate, rails, config_path='config.cfg'):
    config_dict = {}
    config_dict['COM_PORT'] = com_port
    config_dict['BAUD_RATE'] = baud_rate
    config_dict['RAILS'] = rails
    with open(config_path, 'w') as f:
        json.dump(config_dict, f)

'''Returns: com_port:str, baud_rate:str, rails:dict'''
def load_config(config_path='config.cfg') -> tuple:
    if not os.path.isfile(config_path):
        save_config("COM7", "9600", {})
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
    try:
        com_port = config_dict['COM_PORT']
    except:
        raise Exception('Config file does not specify COM_PORT\n    \
                        Add a key value pair to the config file and \
                        try again')
    try:
        baud_rate = config_dict['BAUD_RATE']
    except:
        raise Exception('Config file does not specify BAUD_RATE\n    \
                        Add a key value pair to the config file and \
                        try again')
    try:
        rails = config_dict['RAILS']
    except:
        raise Exception('Config file does not specify RAILS\n    \
                        Add a key value pair to the config file and \
                        try again')
    
    return com_port, baud_rate, rails