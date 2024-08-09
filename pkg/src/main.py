from volume import match_rails_to_apps, set_app_volumes, set_system_volume
import serial
from config_functions import load_config
from threading import Thread
from tray_icon import start_tray_icon, tray_icon_quit_event, serial_unavailable_event
from config_ui import reload_configs_event
from tkinter import messagebox
import time

def open_serial(com_port, baud_rate):
    ser = None

    try:
        ser = serial.Serial(com_port, baud_rate)
        serial_unavailable_event.clear()
    except Exception as e:
        print(e)
        serial_unavailable_event.set()
        messagebox.showerror("VolMan: COM Port Issue",
                f"Unable to read selected COM port. Ensure that {com_port} is correct. Also ensure that {com_port} port is not being used by any other applications. Look in the system tray for the configuration editor.")
    
    return ser

def main():
    com_port, baud_rate, applications = load_config()
    ser = open_serial(com_port, baud_rate)

    # Run system tray in a separate thread
    tray_thread = Thread(target=start_tray_icon, daemon=True)
    tray_thread.start()

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

if __name__ == '__main__':
    main()
