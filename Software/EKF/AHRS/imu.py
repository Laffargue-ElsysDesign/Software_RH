from ahrs.filters import Madgwick, DCM
from numpy.linalg import inv
import numpy as np
gyro_data=np.array([0, 0, 0])
acc_data=np.array([0, 0, 0])
mag_data=np.array([0, 0, 0])
madgwick = Madgwick()
quaternion = np.tile([1., 0., 0., 0.], (len(gyro_data), 1)) # Allocate for quaternions
quaternion = madgwick.updateMARG(quaternion, gyr=gyro_data, acc=acc_data, mag=mag_data)
dcm=DCM(q=quaternion)
print(dcm)
output = np.dot(inv(dcm), acc_data)