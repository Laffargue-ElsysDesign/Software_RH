from signal import signal, SIGINT
from pynq import Overlay
from Constants import DIJKSTRA_MATCH

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

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
    balises = Balises(overlay)
    
    try :
        New, Loc = balises.Check_Balise()
    except:
        print("Balises Lecture failed")