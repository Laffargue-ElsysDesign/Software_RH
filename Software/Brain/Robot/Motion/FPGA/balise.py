from signal import signal, SIGINT
from pynq import Overlay
#from Constants import DIJKSTRA_MATCH
import lib.balise_driver

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
    overlay = Overlay("../Overlays/TimerV1/BitStream/Timer.bit")
    overlay.download()
    balises = Balises(overlay)
    while(1):
        New, Loc = balises.Check_Balise()
        if New:
            print(Loc)
        else:
            print("RAS")