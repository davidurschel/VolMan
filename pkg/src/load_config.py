import json

def load_config(config_path='config.cfg') -> tuple:
    with open(config_path, 'r') as f:
        loaded_dict = json.load(f)
    try:
        com_port = loaded_dict['COM_PORT']
    except:
        raise Exception('Config file does not specify COM_PORT\n    \
                        Add a key value pair to the config file and \
                        try again')
    try:
        baud_rate = loaded_dict['BAUD_RATE']
    except:
        raise Exception('Config file does not specify BAUD_RATE\n    \
                        Add a key value pair to the config file and \
                        try again')
    try:
        rails = loaded_dict['RAILS']
    except:
        raise Exception('Config file does not specify RAILS\n    \
                        Add a key value pair to the config file and \
                        try again')
    
    return com_port, baud_rate, rails