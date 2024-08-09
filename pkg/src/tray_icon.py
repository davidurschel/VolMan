import pystray
from PIL import Image
from threading import Event
import webbrowser
from tools import get_asset_path
import constants
from config_ui import ConfigWindow

tray_icon_quit_event = Event()

current_root = None

def on_config():
    config_ui = ConfigWindow()
    config_ui.geometry("600x500")
    config_ui.mainloop()

def on_help():
    webbrowser.open(constants.HELP_URL)

def on_exit(icon):
    icon.stop()
    tray_icon_quit_event.set()

def start_tray_icon():
    menu = pystray.Menu(
        pystray.MenuItem('Configure', on_config),
        pystray.MenuItem('Help', on_help),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Exit', on_exit)        
    )
    
    icon = pystray.Icon(name="vol_man_volume_manager", 
                        icon=Image.open(get_asset_path(constants.ICON_FILE)), 
                        title="VolMan", 
                        menu=menu)
    icon.visible = False

    icon.run()


if __name__ == "__main__":
    start_tray_icon()