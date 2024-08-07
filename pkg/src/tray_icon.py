import pystray
from PIL import Image
from threading import Event
import webbrowser
import sys
import os

ICON_FILE = 'icon.ico'
HELP_URL = 'https://github.com/davidurschel/VolMan'
tray_icon_quit_event = Event()

def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join('assets', filename)

def on_quit(icon):
    icon.stop()
    tray_icon_quit_event.set()

def on_config():
    print("config")

def on_help():
    webbrowser.open(HELP_URL)

def start_tray_icon():
    menu = pystray.Menu(
        pystray.MenuItem('Configure', on_config),
        pystray.MenuItem('Help', on_help),
        pystray.MenuItem('Quit', on_quit)        
    )
    
    icon = pystray.Icon(name="vol_man_volume_manager", 
                        icon=Image.open(get_asset_path(ICON_FILE)), 
                        title="VolMan", 
                        menu=menu)
    icon.visible = False

    icon.run()

    