import threading
import comtypes
import time
import serial
from tkinter import messagebox
from volume import match_rails_to_apps, set_app_volumes, set_system_volume
from config_functions import load_config
from tray_icon import start_tray_icon, tray_icon_quit_event, serial_unavailable_event
from config_ui import reload_configs_event
import queue


def background_process(alert_queue):
    comtypes.CoInitialize()

    def open_serial(com_port, baud_rate, suppress_alert=False):
        ser = None
        try:
            ser = serial.Serial(com_port, baud_rate)
            serial_unavailable_event.clear()
        except Exception as e:
            print(e)
            serial_unavailable_event.set()
            if not suppress_alert:
                alert_queue.put(("showerror", "VolMan: COM Port Issue",
                f"Unable to read selected COM port. Ensure that {com_port} is correct. Also ensure that {com_port} port is not being used by any other applications. Look in the system tray for the configuration editor."))
        return ser
    com_port, baud_rate, applications = load_config()
    ser = open_serial(com_port, baud_rate)

    while not tray_icon_quit_event.is_set():
        if reload_configs_event.is_set():
            com_port, baud_rate, applications = load_config()
            reload_configs_event.clear()
            try:
                ser.close()
            except:
                pass
            ser = open_serial(com_port, baud_rate)

        if serial_unavailable_event.is_set():
            time.sleep(1)
            ser = open_serial(com_port, baud_rate, suppress_alert=True)
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

def main():
    # Start the background process in a separate thread
    alert_queue = queue.Queue()
    processing_thread = threading.Thread(target=background_process, args=(alert_queue, ))
    processing_thread.start()

    # Start the tray icon on the main thread
    start_tray_icon()

    while True:
        try:
            message = queue.get(block=False)
            if message[0] == "showerror":
                messagebox.showerror(message[1], message[2])
        except queue.Empty:
            pass


if __name__ == '__main__':
    main()
