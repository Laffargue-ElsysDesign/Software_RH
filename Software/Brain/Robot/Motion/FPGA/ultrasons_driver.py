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

    def Read_N_Detection(self):
        return 0 #TBD

    def Read_NW_Detection(self):
        return 0 #TBD

    def Read_NE_Detection(self):
        return 0 #TBD

    def Read_W_Detection(self):
        return 0 #TBD

    def Read_E_Detection(self):
        return 0 #TBD

    def Read_ALL_Detection(self):
        return (self.Read_W_Detection(), self.Read_NW_Detection(), self.Read_N_Detection(), self.Read_NE_Detection(), self.Read_E_Detection()) #TBD

    def Read_N_Zone(self):
        return 0 #TBD

    def Read_NW_Zone(self):
        return 0 #TBD

    def Read_NE_Zone(self):
        return 0 #TBD

    def Read_W_Zone(self):
        return 0 #TBD

    def Read_E_Zone(self):
        return 0 #TBD

    def Read_ALL_Zone(self):
        return (self.Read_W_Zone(), self.Read_NW_Zone(), self.Read_N_Zone(), self.Read_NE_Zone(), self.Read_E_Zone()) #TBD

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
        return (self.Read_W_Value(), self.Read_NW_Value(), self.Read_N_Value(), self.Read_NE_Value(), self.Read_E_Value()) #TBD

   

class Ultrasons():
    def __init__(self, overlay):
        self.ultrasons = overlay.ultrasons_reg #TBD

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
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    ultrasons = Ultrasons()
    
    try :
        if ultrasons.Check_US_State():
            print("Obstacle detected")
    except:
        print("Ronde Lecture failed")