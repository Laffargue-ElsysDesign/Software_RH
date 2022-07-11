from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class BatteryDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Read_State(self):
        return 0 #TBD

class Battery():
    def __init__(self, overlay):
        self.Battery = overlay.battery_reg #TBD

    def Check(self): #TBD
        return self.Battery.Read_State()

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    battery = Battery()
    
    try :
        if battery.Get_New_Alert():
            print("Low Bettery Level")
    except:
        print("Balises Lecture failed")