from signal import signal, SIGINT
from pynq import Overlay
#from Constants import DIJKSTRA_MATCH
import lib.rfid_driver
from time import sleep

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

class RFID():
    def __init__(self, overlay):
        self.rfid = overlay.rfid_0

    def Check_RFID(self):
        (New, Tag) = self.rfid.Read_Rfid()
        #if New:
        #    Loc = self.Get_Dot(Room)
        return (New, Tag)

    #def Get_Dot(self, Value): #TBD
    #    return DIJKSTRA_MATCH[Value, 1]

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/IMUV3/BitStream/IMU.bit")
    overlay.download()
    rfid = RFID(overlay)
    while(1):
        print(rfid.Check_RFID())
        sleep(0.5)