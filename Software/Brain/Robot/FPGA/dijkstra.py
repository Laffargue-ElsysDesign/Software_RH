# dijkstra.py

#  Created on: August 3 2022
#      Author: Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT

######## PYNQ import #########
from pynq import Overlay

########## Driver import #########
#import lib.dijkstra_driver

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)  

class Dijkstra():
    def __init__(self, overlay):
        self.Dijkstra = overlay.Dijkstra_reg_0
    
    def Compute(self, Start, Stop):
        self.Dijkstra.Write_Data(Start, Stop)
        PATH = self.Dijkstra.Read_Data()
        self.Dijkstra.Disable()
        
        return PATH

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US2/BitStream/bitstream.bit")
    overlay.download()
    dijkstra = Dijkstra(overlay)
    
    PATH = dijkstra.Compute(0, 13)
    print(PATH)
    try :
        
        PATH = dijkstra.Compute(0, 17)
    except:
        print("Too long Dijkstra failed")
    PATH = dijkstra.Compute(8, 1)
    print(PATH)
    PATH = dijkstra.Compute(0, 16)
    print(PATH)
    PATH = dijkstra.Compute(7, 4)
    print(PATH)
    PATH = dijkstra.Compute(1, 2)
    print(PATH)
    PATH = dijkstra.Compute(6, 12)
    print(PATH)
    PATH = dijkstra.Compute(15, 9)
    print(PATH)
    PATH = dijkstra.Compute(0, 6)
    print(PATH)