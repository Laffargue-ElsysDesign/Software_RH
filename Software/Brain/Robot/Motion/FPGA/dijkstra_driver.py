from pynq import DefaultIP, Overlay
from signal import signal,SIGINT
import time

OFFSET_WRITE_REG = 0x00
OFFSET_READ_STATUS = 0x04
OFFSET_READ_REG = 0x08
MASK_READ = 0x1F


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class DijkstraDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Dijkstra_reg:1.0']
    
    def Write_Data(self, StartPoint, StopPoint):
        data = (StopPoint << 16) + (StartPoint << 8) + 1
        self.write(OFFSET_WRITE_REG, data)
        
    def Read_Data(self, timeout = 1):
        stop_time = time.time() + timeout
        while (not ((self.read(OFFSET_READ_STATUS) & 1) == 1)) and not (time.time()>stop_time):
            pass
        if time.time()>stop_time:
            raise ValueError("Read timeout")
        nb_nodes = (self.read(OFFSET_READ_REG) & MASK_READ)
        data = []
        print(nb_nodes)
        for i in range(nb_nodes):
            data.append((self.read((OFFSET_READ_REG)+((nb_nodes-i)*4)) & MASK_READ))
        print(data)
        return data 
    
    def Disable(self):
        self.write(OFFSET_WRITE_REG, 0)
        return 1

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
    dijkstra = Dijkstra()
    
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