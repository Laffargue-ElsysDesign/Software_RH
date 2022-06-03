from pynq import Overlay
#import lib.ultrasons_driver
from signal import signal,SIGINT
from time import sleep

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

class Ultrasons():
    def __init__(self, overlay):
        self.ultrasons = overlay.Ultrasons_0 #TBD

    def Check_US_Detection(self): #TBD
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Detection()
        return W, NW, N, NE, E

    def Check_US_Zone(self): #TBD
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Zone()
        return W, NW, N, NE, E

    def Get_Values(self):
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Value()
        return [W, NW, N, NE, E]

    def Enable(self):
        self.ultrasons.Enable()
        return 1

    def Disbale(self):
        self.ultrasons.Disable()
        return 1

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US3/BitStream/bitstream.bit")
    overlay.download()
    ultrasons = Ultrasons(overlay)
    ultrasons.Enable()
    
    while (1):
        print("Detection W NW N NE E : ", ultrasons.Check_US_Detection())
        print("Zone W NM N NE E : ", ultrasons.Check_US_Zone())
        print("Values W NM N NE E : ", ultrasons.Get_Values())
        print()
        sleep(2)