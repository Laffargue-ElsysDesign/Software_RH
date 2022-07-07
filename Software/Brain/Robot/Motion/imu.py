from ahrs.filters import Madgwick, DCM
from ahrs.utils import WMM
from numpy.linalg import inv
import numpy as np


def myWMM():
    #Magnetic Declination and gravity offset
    lat = 43.5687
    lon = 1.38735
    wmm = WMM()
    wmm.magnetic_field(lat, lon, height=0.165)
    print(wmm.D)
    return wmm

def Compass_Acc():
    pass #TBD

def myAHRS():
    

    #DCM and IMU manipulation
    gyro_data=np.array([0, 0, 0])
    acc_data=np.array([0, 0, 0])
    mag_data=np.array([0, 0, 0])
    madgwick = Madgwick()
    quaternion = np.tile([1., 0., 0., 0.], (len(gyro_data), 1)) # Allocate for quaternions
    quaternion = madgwick.updateMARG(quaternion, gyr=gyro_data, acc=acc_data, mag=mag_data)
    dcm=DCM(q=quaternion)
    print(dcm)
    output = np.dot(inv(dcm), acc_data)

    wmm = myWMM()
    
    return Compass_Acc()

