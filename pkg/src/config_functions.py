import json
import os
import constants

def get_config_path(CONFIG_FILENAME):
    app_data_path = os.getenv('APPDATA')
    return os.path.join(app_data_path, 'VolMan', CONFIG_FILENAME)

def save_config(com_port, baud_rate, rails, config_filename=constants.CONFIG_FILENAME):
    config_dict = {}
    config_dict['COM_PORT'] = com_port
    config_dict['BAUD_RATE'] = baud_rate
    config_dict['RAILS'] = rails
    with open(get_config_path(config_filename), 'w') as f:
        json.dump(config_dict, f)
        f.close()

'''Returns: com_port:str, baud_rate:str, rails:dict'''
def load_config(config_filename=constants.CONFIG_FILENAME) -> tuple:
    if not os.path.isfile(get_config_path(config_filename)):
        save_config("", "", {})
    config_dict = {'COM_PORT': '', 'BAUD_RATE': '', 'RAILS':''}
    try:
        with open(get_config_path(config_filename), 'r') as f:
            config_dict = json.load(f)
            f.close()
    except: 
        pass

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
    
    return (com_port, baud_rate, rails)