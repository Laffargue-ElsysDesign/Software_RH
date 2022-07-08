from pynq import DefaultIP, Overlay
from signal import signal,SIGINT

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class IMUDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Read_acc(self):
        return (0, 0, 0) #TBD
        
    def Read_gyr(self):
        return (0, 0, 0) #TBD
    
    def Read_mag(self):
        return (0, 0, 0) #TBD

    def Read_data(self):
        (ax, ay, az) = self.Read_acc()
        (gx, gy, gz) = self.Read_gyr()
        (mx, my, mz) = self.Read_mag()
        return (ax, ay, az, gx, gy, gz, mx, my, mz)

class IMU():
    def __init__(self, overlay):
        self.imu = overlay.balise_reg #TBD
    
    def Get_data(self):
        return self.imu.Read_data()

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    imu = IMU()
    
    try :
        print(imu.Get_data())
    except:
        print("Balises Lecture failed")