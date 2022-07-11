from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class RondeDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Timer_ronde:1.0']
    
    def Read_State(self):
        state = self.read(OFFSET_READ_STATE & 1)
        return state

    def Reset(self):
        while self.read((OFFSET_READ_STATE & 1) != 0):
            self.write(OFFSET_RESET, 1)
        self.write(OFFSET_RESET, 0)
        return 1

class Ronde():
    def __init__(self, overlay):
        self.Ronde = overlay.Timer_ronde_0 

    def Check(self): #TBD
        New_Alert = self.Ronde.Read_State()
        if New_Alert:
            self.Ronde.Reset()
        return New_Alert

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