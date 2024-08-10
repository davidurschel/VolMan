import pystray
from PIL import Image
from threading import Event, Thread
import webbrowser
import subprocess
import os
from tools import get_asset_path
import constants

tray_icon_quit_event = Event()
reload_configs_event = Event()
editing_configs_event = Event()

def on_config():
    if editing_configs_event.isSet():
        return
    
    def run_in_thread():
        editing_configs_event.set()
        proc = subprocess.Popen("VolMan_Config_Editor.exe")
        proc.wait()
        editing_configs_event.clear()
        reload_configs_event.set()
        return
    
    thread = Thread(target=run_in_thread)
    thread.start()
    
    


def on_help():
    webbrowser.open(constants.HELP_URL)

def on_exit(icon):
    icon.stop()
    tray_icon_quit_event.set()

def start_tray_icon():
    menu = pystray.Menu(
        pystray.MenuItem('Configure', lambda: on_config()),
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
