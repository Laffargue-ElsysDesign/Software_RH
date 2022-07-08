from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

LOC_ENTREE = 1 #TBD
LOC_STAGIAIRE = 2 #TBD
LOC_MANAGER = 3 #TBD
LOC_PAUSE = 4 #TBD
LOC_REUNION = 5 #TBD
LOC_BUREAU = 6 #TBD
LOC_OPENSPACE = 7 #TBD

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
        
    def Read_Balise(self, timeout = 1):
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
        self.New_Alert = False
        self.Loc = 0
        self.Balises = overlay.balise_reg #TBD
    
    def Check_Balises(self):
        (self.New_Alert, self.Loc) = self.Balises.Read_Balise()

    def Is_New_Alert(self):
        return self.New_Alert

    def Get_Loc(self): #TBD
        Value = self.Loc
        if Value == 1:
            Loc = LOC_ENTREE
        elif Value == 2:
            Loc = LOC_STAGIAIRE
        elif Value == 3:
            Loc = LOC_MANAGER
        elif Value == 4:
            Loc = LOC_PAUSE
        elif Value == 5:
            Loc = LOC_REUNION
        elif Value == 6:
            Loc = LOC_BUREAU
        elif Value == 7:
            Loc = LOC_OPENSPACE
        self.Reset()
        return Loc

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