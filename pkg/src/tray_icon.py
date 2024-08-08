import pystray
from PIL import Image
from threading import Event
import webbrowser
import sys
import os
import subprocess
import constants
import tkinter as tk

tray_icon_quit_event = Event()

current_root = None

def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join('assets', filename)

def on_exit(icon):
    icon.stop()
    tray_icon_quit_event.set()

def ok_button_clicked(root):
    root.destroy()

def open_config_help_link():
    webbrowser.open(constants.CONFIG_HELP_URL)

def config_dialog():
    global current_root

    if current_root is not None:
        try:
            current_root.destroy()
        except tk.TclError:
            pass

    current_root = tk.Tk()
    current_root.withdraw()

    dialog = tk.Toplevel(current_root)
    dialog.title("VolMan Config Info")

    icon_photo = tk.PhotoImage(file=get_asset_path(constants.ICON_FILE))
    current_root.iconphoto(False, icon_photo)
    dialog.iconphoto(False, icon_photo)

    message = tk.Label(dialog, text="To configure your VolMan setup you have to edit the config.cfg file. For more information click the More Info button. To proceed click the OK button.", wraplength=300)
    message.pack(padx=20, pady=10)
    frame = tk.Frame(dialog)
    frame.pack(pady=10)

    button_width = 15
    button_height = 2
    link_button = tk.Button(frame, text="More Info", command=open_config_help_link, width=button_width, height=button_height)
    link_button.pack(side=tk.LEFT, padx=5)
    ok_button = tk.Button(frame, text="OK", command=lambda: ok_button_clicked(current_root), width=button_width, height=button_height)
    ok_button.pack(side=tk.RIGHT, padx=5)

    current_root.mainloop()


def on_config():
    current_dir = os.getcwd()
    subprocess.Popen(f'explorer {current_dir}')
    config_dialog()
    

def on_help():
    webbrowser.open(constants.HELP_URL)

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
    on_config()