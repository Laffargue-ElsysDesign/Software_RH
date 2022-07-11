from pynq import DefaultIP, Overlay
from signal import signal,SIGINT
from Constants import DIJKSTRA_MATCH
import time

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04
OFFSET_READ_BALISE = 0x08
MASK_BALISE = 0x0F


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class BaliseDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise:1.0']
    
    def Read_State(self):
        state = self.read(OFFSET_READ_STATE & 1)
        return state
        
    def Read_Loc(self, timeout = 1):
        Loc = self.read(OFFSET_READ_BALISE & MASK_BALISE)
        return Loc 
    
    def Reset(self):
        while self.read(OFFSET_READ_STATE & 1) != 0)):
            self.write(OFFSET_RESET, 1)
        self.write(OFFSET_RESET, 0)
        return 1

    def Read_Balise(self):
        Loc = 0
        New = False
        if (self.Read_State() == 1):
            New = True
            Loc = self.Read_Loc()
            self.Reset()
        return (New, Loc)

class Balises():
    def __init__(self, overlay):
        self.balises = overlay.balise_0

    def Check_Balise(self):
        (New, Room) = self.balises.Read_Balise()
        if New:
            Loc = self.Get_Dot(Room)
        return (New, Loc)

    def Get_Dot(self, Value): #TBD
        return DIJKSTRA_MATCH[Value, 1]

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    balises = Balises()
    
    try :
        balises.Check_Balises()
        if balises.Is_New_Alert():
            Loc = balises.Get_Loc()
    except:
        print("Balises Lecture failed")