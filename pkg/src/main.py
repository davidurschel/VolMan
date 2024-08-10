import threading
from tray_icon import start_tray_icon
from volume_loop import volume_loop

def main():
    # Run volume_loop in a separate thread
    volume_thread = threading.Thread(target=volume_loop)
    volume_thread.start()
    
    # Start the tray icon in the main thread
    start_tray_icon()

if __name__ == '__main__':
    main()
