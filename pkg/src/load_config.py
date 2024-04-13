import json

def load_config(config_path="config.cfg") -> tuple:
    with open(config_path, "r") as f:
        loaded_dict = json.load(f)
    
    try:
        com_port = loaded_dict["COM_PORT"]
    except:
        raise Exception("Config file does not specify COM_PORT\n    \
                        Add a key value pair to the config file and \
                        try again")

    try:
        baud_rate = loaded_dict["BAUD_RATE"]
    except:
        raise Exception("Config file does not specify BAUD_RATE\n    \
                        Add a key value pair to the config file and \
                        try again")
    
    rails = loaded_dict

    return com_port, baud_rate, rails

with open("config.cfg", "w") as f:
    json.dump({'COM_PORT': 'COM4',
               'BAUD_RATE': 9600,
               'RAILS': {"1": ["discord.exe", "valorant.exe"]}}, f, indent=4)

print(load_config())