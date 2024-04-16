from volume import match_rails_to_apps, set_app_volumes, set_system_volume
import serial
from load_config import load_config

def main():
    com_port, baud_rate, applications = load_config()

    ser = serial.Serial(com_port, baud_rate)

    while True:
        # Catch errors if the Serial bitstream is misalligned
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

if __name__ == '__main__':
    main()
