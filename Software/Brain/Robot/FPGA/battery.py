# battery.py

#  Created on: August 3 2022
#      Author: Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT

######## PYNQ import #########
from pynq import Overlay

########## Driver import #########
#import lib.battery_driver

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

class Battery():
    def __init__(self, overlay):
        self.Battery = overlay.battery_reg #TBD

    def Check(self): #TBD
        return self.Battery.Read_State()

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US2/BitStream/bitstream.bit")
    overlay.download()
    battery = Battery(overlay)
    
    try :
        if battery.Check():
            print("Low Bettery Level")
    except:
        print("Balises Lecture failed")