from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class UltrasonsDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Enable(self):
        return 0 #TBD

    def Disable(self):
        return 0 #TBD

    def Read_N_State(self):
        return 0 #TBD

    def Read_NW_State(self):
        return 0 #TBD

    def Read_NE_State(self):
        return 0 #TBD

    def Read_W_State(self):
        return 0 #TBD

    def Read_E_State(self):
        return 0 #TBD

    def Read_ALL_State(self):
        return (self.Read_N_State(), self.Read_E_State(), self.Read_NE_State(), self.Read_NW_State(), self.Read_W_State()) #TBD

    def Read_N_Value(self):
        return 0 #TBD

    def Read_NW_Value(self):
        return 0 #TBD

    def Read_NE_Value(self):
        return 0 #TBD

    def Read_W_Value(self):
        return 0 #TBD

    def Read_E_Value(self):
        return 0 #TBD

    def Read_ALL_Value(self):
        return (self.Read_N_Value(), self.Read_E_Value(), self.Read_NE_Value(), self.Read_NW_Value(), self.Read_W_Value()) #TBD

   

class Ultrasons():
    def __init__(self, overlay):
        self.N = 0
        self.E = 0
        self.W = 0
        self.NE = 0
        self.NW = 0
        self.ultrasons = overlay.ultrasons_reg #TBD

    def Check_US_State(self): #TBD
        (self.N, self.E, self.NE, self.NW, self.W) = self.ultrasons.Read_ALL_State()
        return 1

    def Get_Values(self):
        (N, E, NE, NW, W) = self.ultrasons.Read_ALL_Value()
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
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    ultrasons = Ultrasons()
    
    try :
        if ultrasons.Check_US_State():
            print("Obstacle detected")
    except:
        print("Ronde Lecture failed")