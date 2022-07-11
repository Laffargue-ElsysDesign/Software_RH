from pynq import Overlay
from signal import signal,SIGINT

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)  

class Dijkstra():
    def __init__(self):
        self.Dijkstra = overlay.Dijkstra_reg_0
    
    def Compute(self, Start, Stop):
        self.Dijkstra.Write_Data(self.start, self.stop)
        PATH = self.Dijkstra.Read_Data()
        self.Dijkstra.Disable()
        
        return PATH

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    dijkstra = Dijkstra(overlay)
    
    PATH = dijkstra.Compute(0, 13)
    try :
        
        PATH = dijkstra.Compute(0, 17)
    except:
        print("Too long Dijkstra failed")
    PATH = dijkstra.Compute(8, 1)
    PATH = dijkstra.Compute(0, 16)
    PATH = dijkstra.Compute(7, 4)
    PATH = dijkstra.Compute(1, 2)
    PATH = dijkstra.Compute(6, 12)
    PATH = dijkstra.Compute(15, 9)