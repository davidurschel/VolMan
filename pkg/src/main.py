from volume import SetSystemVolume, SetApplicationVolume, SetApplicationVolumes, GetActiveVolumeSessions
import serial
from load_config import load_config

def main():
    com_port, baud_rate, applications = load_config()

    ser = serial.Serial(com_port, baud_rate)

    while True:
        # Catch errors if the Serial bitstream is misalligned
        try:
            data = ser.readline().decode().strip()
            sep = data.split("|")
            print("Received:", sep)

            # Set the volume for all the programs as configured
            # SetSystemVolume(100 * volume_value)
        except ValueError as e:
            print("Error parsing data:", e)
        except Exception as e:
            print("An error occurred:", e)
    return

if __name__ == "__main__":
    main()
