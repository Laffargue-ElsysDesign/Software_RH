from tkinter import E
import Robot.Motion.holo32.holo_uart_management as HUM 
from Robot.ManualControl import thread_manual_control
from time import sleep, time
from threading import Thread, Lock
from signal import signal, SIGINT
from pynq import Overlay


#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

#app=Create_App()
if __name__ == '__main__':
    signal(SIGINT, handler)

    global overlay
    overlay=Overlay("./Robot/Motion/Overlays/IMUV2/BitStream/IMU.bit", download=False)
    if overlay.is_loaded()==False:
        print("Loading Overlay...")
        overlay.download()
    
    print('Bring up uart....')
    
    #app.run(debug = True)

    thread_holo = HUM.Holo_UART(overlay)
    thread_holo.start()

    thread_manual_control.start()
    
    thread_manual_control.mgt.Restart()
