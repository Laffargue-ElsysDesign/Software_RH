from curses import raw
from Software.Brain.Robot.Motion.FPGA.lib.imu_driver import X_MAG_OFFSET, Y_ACC_OFFSET
from pynq import Overlay
import lib.imu_driver
from signal import signal,SIGINT
from time import sleep

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

class IMU():
    def __init__(self, overlay):
        self.imu = overlay.IP_IMU_0
        self.X_ACC_OFFSET = 0
        self.Y_ACC_OFFSET = 0
        self.Z_GYRO_OFFSET = 0
        self.X_MAG_OFFSET = 0
        self.Y_MAG_OFFSET = 0
        self.Z_MAG_OFFSET = 0
    
    def Get_Data(self):
        raw_data = self.Get_Raw_Data()
        raw_data[0] -= self.X_ACC_OFFSET
        raw_data[1] -= self.Y_ACC_OFFSET
        raw_data[5] -= self.Z_GYRO_OFFSET
        raw_data[6] += self.X_MAG_OFFSET/1000000
        raw_data[7] += self.Y_MAG_OFFSET/1000000
        raw_data[8] += self.Z_MAG_OFFSET/1000000
        return raw_data
    
    def Get_Raw_Data(self):
        return self.imu.Read_Data()

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/IMUV1/BitStream/IMU.bit")
    overlay.download()
    imu = IMU(overlay)
    while(1):
        print(imu.Get_Raw_Data())
        sleep(0.3)