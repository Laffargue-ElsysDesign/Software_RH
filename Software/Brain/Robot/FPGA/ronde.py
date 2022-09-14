# ronde.py

#  Created on: August 3 2022
#      Author: Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT
from time import time, sleep

######## PYNQ import #########
from pynq import Overlay

########## Driver import #########
#import lib.ronde_driver


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
    
    def Set_2_min(self):
        self.Ronde.Config_Timer(SECONDS, TWO)

    def Set_2_hour(self):
        self.Ronde.Config_Timer(MINUTES, TWO)
    
    def Config_Timer(self, seconds, count):
        self.Ronde.Config_Timer(seconds, count)

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US2/BitStream/bitstream.bit")
    overlay.download()
    ronde = Ronde(overlay)
    ronde.Set_2_min()
    i=0
    while(1):
        sleep(1)
        print(i)
        i+=1
        if ronde.Check():
            print("New Ronde", time())
        else:
            print("No Ronde Asked")

