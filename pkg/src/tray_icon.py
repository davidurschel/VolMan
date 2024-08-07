import pystray
from PIL import Image
from threading import Event
import webbrowser

ICON_PATH = 'assets/icon.png'
HELP_URL = 'https://github.com/davidurschel/VolMan'
tray_icon_quit_event = Event()

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
                        icon=Image.open(ICON_PATH), 
                        title="VolMan", 
                        menu=menu)
    icon.visible = False

    icon.run()

    