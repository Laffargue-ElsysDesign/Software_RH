from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class RondeDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Read_State(self):
        return 0 #TBD

    def Reset():
        return 0 #TBD

class Ronde():
    def __init__(self, overlay):
        self.New_Alert = False
        self.Ronde = overlay.ronde_reg #TBD
    
    def Get_New_Alert(self):
        return self.New_Alert

    def Check(self): #TBD
        self.New_Alert = self.Ronde.Read_State()
        if self.New_Alert:
            self.Ronde.Reset()
        return 0

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    ronde = Ronde()
    
    try :
        if ronde.Get_New_Alert():
            print("New Ronde")
    except:
        print("Ronde Lecture failed")