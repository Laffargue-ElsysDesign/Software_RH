# imu_driver.py

#  Created on: July 8 2022
#      Author: Isabelle Van Leeuwen and Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT
import numpy as np

######## PYNQ import #########
from pynq import DefaultIP


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
X_GYRO_OFFSET = 0
Y_GYRO_OFFSET = 0
Z_GYRO_OFFSET = 0
X_ACC_OFFSET = 0
Y_ACC_OFFSET = 0
Z_ACC_OFFSET = 0

# ========== Accès IP IMU ==========
OFFSET_READ_ACC_X = 0x00
OFFSET_READ_ACC_Y = 0x04
OFFSET_READ_ACC_Z = 0x08

OFFSET_READ_GYR_X = 0x0C
OFFSET_READ_GYR_Y = 0x10
OFFSET_READ_GYR_Z = 0x14

OFFSET_READ_MAG_X = 0x18
OFFSET_READ_MAG_Y = 0x1C
OFFSET_READ_MAG_Z = 0x20

MASQUE = 0xFFFF                       

class IMUDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:IMU_v3:1.0']
    
    def Read_acc(self):
        raw_acc_x = self.read(OFFSET_READ_ACC_X)
        raw_acc_y = self.read(OFFSET_READ_ACC_Y)
        raw_acc_z = self.read(OFFSET_READ_ACC_Z)
        #print("Acc:", hex(raw_acc_x), hex(raw_acc_y))
        acc_x = np.int16(raw_acc_x & MASQUE) * (G/SENS_ACC)
        acc_y = np.int16(raw_acc_y & MASQUE) * (G/SENS_ACC)
        acc_z = np.int16(raw_acc_z & MASQUE) * (G/SENS_ACC)
        return (acc_x, acc_y, acc_z)
        
    def Read_gyr(self):
        raw_gyr_x = self.read(OFFSET_READ_GYR_X)
        raw_gyr_y = self.read(OFFSET_READ_GYR_Y)
        raw_gyr_z = self.read(OFFSET_READ_GYR_Z)
        #print("Gyr:", hex(raw_gyr_z))
        gyr_x = -(2*np.pi/360 * np.int16(raw_gyr_x & MASQUE) )/ SENS_GYRO - X_GYRO_OFFSET
        gyr_y = -(2*np.pi/360 * np.int16(raw_gyr_y & MASQUE) )/ SENS_GYRO - Y_GYRO_OFFSET
        gyr_z = -(2*np.pi/360 * np.int16(raw_gyr_z & MASQUE) )/ SENS_GYRO - Z_GYRO_OFFSET
        return (gyr_x, gyr_y, gyr_z)
    
    def Read_mag(self):
        raw_mag_x = (self.read(OFFSET_READ_MAG_X))
        raw_mag_y = (self.read(OFFSET_READ_MAG_Y))
        raw_mag_z = (self.read(OFFSET_READ_MAG_Z))
        #print("Mag:", hex(raw_mag_x), hex(raw_mag_y), hex(raw_mag_z))
        mag_x = (np.int16(raw_mag_x & MASQUE) * 0.15)/1000000
        mag_y = (np.int16(raw_mag_y & MASQUE) * 0.15)/1000000
        mag_z = (np.int16(raw_mag_z & MASQUE) * 0.15)/1000000
        return (mag_x, mag_y, mag_z)

    def Read_Data(self):
        (ax, ay, az) = self.Read_acc()
        (gx, gy, gz) = self.Read_gyr()
        (mx, my, mz) = self.Read_mag()
        return [ax, ay, az, gx, gy, gz, mx, my, mz]