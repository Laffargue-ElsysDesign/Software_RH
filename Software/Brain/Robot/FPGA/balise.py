# balise.py

#  Created on: August 3 2022
#      Author: Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT
from time import sleep

######## PYNQ import #########
from pynq import Overlay

########## Driver import #########
#import lib.balise_driver

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

class Balises():
    def __init__(self, overlay):
        self.balises = overlay.Balise_0

    def Check_Balise(self):
        (New, Room) = self.balises.Read_Balise()
        #if New:
        #    Loc = self.Get_Dot(Room)
        return (New, Room)

    #def Get_Dot(self, Value): #TBD
    #    return DIJKSTRA_MATCH[Value, 1]

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US2/BitStream/bitstream.bit")
    overlay.download()
    balises = Balises(overlay)
    while(1):
        print(balises.Check_Balise())
        sleep(0.5)