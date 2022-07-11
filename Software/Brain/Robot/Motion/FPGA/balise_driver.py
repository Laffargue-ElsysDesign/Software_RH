from pynq import DefaultIP, Overlay
from signal import signal,SIGINT
from Constants import DIJKSTRA_MATCH




def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class BaliseDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Read_State(self):
        return 0 #TBD
        
    def Read_Loc(self, timeout = 1):
        return(0) #TBD
    
    def Reset(self):
        return 0 #TBD

    def Read_Balise(self):
        Loc = 0
        New = False
        if (self.Read_State()):
            New = True
            Loc = self.Read_Balise()
            self.Reset()
        return (New, Loc)

class Balises():
    def __init__(self, overlay):
        self.balises = overlay.balise_reg #TBD

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