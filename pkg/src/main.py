from volume import SetSystemVolume, SetApplicationVolume, SetApplicationVolumes, GetActiveVolumeSessions
import serial


COM_PORT = 'COM4'
BAUD_RATE = 9600 


def main():
    ser = serial.Serial(COM_PORT, BAUD_RATE)

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
