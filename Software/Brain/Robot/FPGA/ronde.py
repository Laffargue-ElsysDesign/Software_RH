from pynq import Overlay
from signal import signal,SIGINT
import lib.ronde_driver
from time import time, sleep

SECONDS = True
MINUTES = False
TWO = 120

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

class Ronde():
    def __init__(self, overlay):
        self.Ronde = overlay.Timer_ronde_0 

    def Check(self): #TBD
        New_Alert = self.Ronde.Read_State()
        if New_Alert:
            self.Ronde.Reset()
        return New_Alert
    
    def Set_2_hour(self):
        self.Ronde.Config_Timer(SECONDS, TWO)

    def Set_2_min(self):
        self.Ronde.Config_Timer(MINUTES, TWO)
    
    def Config_Timer(self, seconds, count):
        self.Ronde.Config_Timer(seconds, count)

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/IMUV1/BitStream/IMU.bit")
    overlay.download()
    ronde = Ronde(overlay)
    i=0
    while(1):
        sleep(1)
        print(i)
        i+=1
        if ronde.Check():
            print("New Ronde", time())
        else:
            print("No Ronde Asked")

