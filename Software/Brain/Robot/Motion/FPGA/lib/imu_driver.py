from pynq import DefaultIP
import numpy as np

# ========== Parametre global IMU ==========
G = 9.80665
SENS_ACC = 16384 #sensibilite accelerometre en lsb/g cf datasheet
SENS_GYRO = 131 #sensibilite gyroscope en lsb/dps cf datasheet

global X_MAG_OFFSET
global Y_MAG_OFFSET
X_MAG_OFFSET = 0
Y_MAG_OFFSET = 0
Z_MAG_OFFSET = 0

global Z_GYRO_OFFSET
global X_ACC_OFFSET
global Y_ACC_OFFSET
Z_GYRO_OFFSET = 0
X_ACC_OFFSET = 0
Y_ACC_OFFSET = 0

# ========== Accès IP IMU ==========
OFFSET_READ_ACC_X = 0x00
OFFSET_READ_ACC_Y = 0x04

OFFSET_READ_GYR_Z = 0x08

OFFSET_READ_MAG_X = 0x0C
OFFSET_READ_MAG_Y = 0x10
OFFSET_READ_MAG_Z = 0x14

MASQUE = 0xFFFF                       

class IMUDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:IP_IMU:1.0']
    
    def Read_acc(self):
        acc_x = (self.read(OFFSET_READ_ACC_X) & MASQUE) * (G/SENS_ACC)
        acc_y = (self.read(OFFSET_READ_ACC_Y) & MASQUE) * (G/SENS_ACC)
        acc_z = -G
        return (acc_x, acc_y, acc_z)
        
    def Read_gyr(self):
        gyr_x = 0
        gyr_y = 0
        gyr_z = -(2*np.pi/360 * (self.read(OFFSET_READ_GYR_Z) & MASQUE) )/ SENS_GYRO - Z_GYRO_OFFSET
        return (gyr_x, gyr_y, gyr_z)
    
    def Read_mag(self):
        mag_x = ((self.read(OFFSET_READ_MAG_X) & MASQUE) * 0.15)/1000000
        mag_y = ((self.read(OFFSET_READ_MAG_Y) & MASQUE) * 0.15)/1000000
        mag_z = ((self.read(OFFSET_READ_MAG_Z) & MASQUE) * 0.15)/1000000
        return (mag_x, mag_y, mag_z)

    def Read_data(self):
        (ax, ay, az) = self.Read_acc()
        (gx, gy, gz) = self.Read_gyr()
        (mx, my, mz) = self.Read_mag()
        return [ax, ay, az, gx, gy, gz, mx, my, mz]