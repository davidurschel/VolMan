import time
import comtypes
import serial
from threading import Event
from win11toast import toast
from volume import match_rails_to_apps, set_app_volumes, set_system_volume
from config_functions import load_config
from tray_icon import tray_icon_quit_event, reload_configs_event
from tools import open_help_url

serial_unavailable_event = Event()

def open_serial(com_port, baud_rate, ser=None, suppress_alert=False):
        if ser:
            try:
                ser.close()
            except Exception as e:
                print(e)

        try:
            ser = serial.Serial(com_port, baud_rate)
            serial_unavailable_event.clear()
        except Exception as e:
            print(e)
            serial_unavailable_event.set()
            if not suppress_alert:
                toast("VolMan: COM Port Issue",
                  f"Unable to open the selected COM port. Ensure that {com_port} is correct. Also ensure that {com_port} port is not being used by any other applications. Look in the system tray for the configuration editor.",
                  on_click=lambda _: open_help_url())
        return ser

def volume_loop():
    com_port, baud_rate, applications = load_config()
    comtypes.CoInitialize()
    ser = open_serial(com_port, baud_rate)

    while not tray_icon_quit_event.is_set():
        if reload_configs_event.is_set():
            com_port, baud_rate, applications = load_config()
            reload_configs_event.clear()
            ser = open_serial(com_port, baud_rate, ser=ser)

        if serial_unavailable_event.is_set():
            time.sleep(1)
            ser = open_serial(com_port, baud_rate, ser=ser, suppress_alert=True)
            continue

        # Catch errors if the Serial bitstream is misaligned
        try:
            data = ser.readline().decode().strip()
            rails = data.split('|')

            app_volumes = match_rails_to_apps(rails, applications)  
            if "MASTER" in app_volumes:
                set_system_volume(app_volumes["MASTER"])

            # Set the volume for all the programs as configured
            set_app_volumes(app_volumes)

        except ValueError as e:
            print('Error parsing data:', e)
        except Exception as e:
            print('An error occurred:', e)
    ser.close()
    comtypes.CoUninitialize()