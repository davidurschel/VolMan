import os
import sys
import constants
import webbrowser

def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join('assets', filename)

def open_help_url():
    webbrowser.open(constants.HELP_URL)