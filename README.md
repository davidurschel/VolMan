# VolMan
VolMan gives a hardware interface to allow users to control the volume on your windows device using physical controls, offering a more intuitive and responsive method than the on-screen alternative. This is done by leverating an arduino microcontroller and physical slider or knob potentiometers as well as a native windows application written in python. The arduino reads the resistances of the potentiometers and passes these to your windows device via serial connection where they are read and the system or application volume is changed in real time. VolMan also allows for users to update the configuration in real time using the system tray icon provided. This project includes the circuit layout, 3D models for a case, Arduino code, and a windows exectuable with setup instructions below.

## Setup
### Physical Setup
#### Breadboard
Using a breadboard is the easiest way to setup VolMan

Layout the circuit so that all potentiometers you are using are being read by the analog pins of your arduino:
- The voltage across the potentiometer should be from the arduinos 5V to the arduinos Ground pin
  
This is the circuit Layout for a design using an Arduino nano and 5 sliding 75mm Potentiometers

![image](https://github.com/user-attachments/assets/e02fd8b8-3e23-4ab4-b99d-06a012418484)

#### 5 Rail With 3D Models
Still testing... will update with instructions once known to be working

### Arduino Setup
To setup the arduino to be connected to a serial COM port you can flash it with the [Default Script](https://github.com/davidurschel/VolMan/blob/main/arduino/main/main.ino)
- Make sure to that all Analog pins with attached potentiometers are in the potPins list
- Adjust the BAUD rate of the signal if you like

If you are writing a custom script, the only thing that you need to make sure is that the arduinos output over serial is of the same form:
- Every rail is a Float between 0 and 1
- Rails are seperated by the pipe symbol "|"
- All rails are printed on the same line, and new measurements are sent on a new line

For example for a setup with 5 rails the serial output should be like this:

![image](https://github.com/user-attachments/assets/6b423afc-a4dc-4cef-9b9f-efb5771def85)


### Windows Setup
To set up VolMan in windows head to the releases section on this github and download the [VolMan Installer](https://github.com/davidurschel/VolMan/releases/latest)
After installing VolMan using the installer you can configure the device from the VolMan icon in the system tray

![image](https://github.com/user-attachments/assets/64b71e05-fb8b-4bfb-b0cb-51fb04875ba8)

Right click the VolMan icon and open the configure GUI

![image](https://github.com/user-attachments/assets/13a678af-83c4-4720-93fe-4d51ae26c39d)

Using this GUI you can configure the setup of VolMan
- Set the COM Port match the COM port to that which your arduino is connected to. This can be checked by right clicking on the windows icon and looking for it in the decvice mangaer
- Set the BAUD Rate to match the BAUD rate that you chose to send serial data in your arduino script
- The number of rails should be the number of potentiometers you have connected to your arduino and the same as the number of unique numbers being sent through serial from the arduino 

Adding applications to rails is also done with this GUI
- To control the volume of a specific application enter the full name of the file and add it, eg. discord.exe
- MASTER: can be added with Add Master; controls the system volume
- OTHER: can be added with Add Other; controls the volume of all applications not specifically assigned to any rails

![image](https://github.com/user-attachments/assets/507688fa-a5d2-4050-9457-bb959fc00821)


