# -*- coding: utf-8 -*-
from threading import Thread, Lock
import matplotlib.pyplot as plt
import numpy as np
from time import time, sleep
from Robot.holo32.holo_uart_management import odometry

"""
Created on Mon Jun 27 08:32:09 2022

@author: laffargue
"""

class Coordinate:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

        self.MUT = Lock()
    
    def Write_Loc(self, X, Y, angle):
        self.MUT.acquire()
        self.x = X
        self.y = Y
        self.angle = angle
        self.MUT.release()

    def Get_Angle(self):
        self.MUT.acquire()
        angle = self.angle
        self.MUT.release()
        return angle

coordinate = Coordinate()

class IMU_Data():
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.theta = 0
        self.MUT = Lock()
    
    def Write(self,ax, ay, theta):
        self.MUT.acquire()
        self.ax = ax
        self.ay = ay
        self.theta = theta
        self.MUT.release()
        
    def Read(self):
        self.MUT.acquire()
        ax = self.ax
        ay = self.ay
        theta = self.theta
        self.MUT.release()
        return ax, ay, theta
    
imu_data = IMU_Data()

def cos(a):
    return np.cos(a*np.pi/180)

def sin(a):
    return np.sin(a*np.pi/180)

class Filter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.NFC_Alert = False
        self.point = 0
        self.position = 0
        self.interrupt = False

    def Interrupt(self):
        self.interrupt = True

    def initialize(self, x, y, z, vx, vy, vz, ax, ay, dt, Sigma_odom, Sigma_acc, Sigma_gyro, err_N_dot, err_N_dot_dot, err_E_dot, err_E_dot_dot, err_theta_dot):
        A = np.array([[1, dt, (dt**2)/2, 0, 0, 0, 0, 0],
                     [0, 1, dt, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0],
                     [0 ,0 ,0 ,1 , dt, (dt*2)/2, 0, 0],
                     [0, 0, 0, 0, 1, dt, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, dt],
                     [0, 0, 0, 0, 0, 0, 0, 1]])
        
        X = np.array([[x],
                      [vx],
                      [ax],
                      [y], 
                      [vy], 
                      [ay], 
                      [z],
                      [vz]])
        
        R = np.array([[Sigma_odom, 0, 0, 0, 0, 0],
                     [0, Sigma_odom, 0, 0, 0, 0],
                     [0, 0, Sigma_acc, 0, 0, 0],
                     [0, 0, 0, Sigma_acc, 0, 0],
                     [0, 0, 0, 0, Sigma_odom, 0],
                     [0, 0, 0, 0, 0, Sigma_gyro]])
       
        Q = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, err_N_dot, 0, 0, 0, 0, 0, 0],
                     [0, 0, err_N_dot_dot, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, err_E_dot, 0, 0, 0],
                     [0, 0, 0, 0, 0, err_E_dot_dot, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, err_theta_dot]])
        
        P = np.eye(8)*0.405
        
        return (A, X, R, Q, P)
    
    def measurement(self):
        #words = line.split()
        R_ax, R_ay, R_gz = odometry.Read()
        R_vx, R_vy, R_vz = imu_data.Read()
        
        ax = -(float(R_ay))*0.01
        ay = float(R_ax)*0.01
        theta_dotGz = 2*np.pi/360*float(R_gz)
        vx = R_vx*0.89
        vy = R_vy*0.89
        theta_dotOz = R_vz*0.62
        print(vx, vy, ax, ay, theta_dotOz, theta_dotGz)
        return np.array([[vx], [vy], [ax], [ay], [theta_dotOz], [theta_dotGz]])
    
    def predict(self, X, A, P, Q):
        X_hat = np.dot(A, X)
        X_hat[6, 0] = X_hat[6, 0] % 360
        P_hat = np.dot(np.dot(A, P), A.transpose()) + Q
        return (X_hat, P_hat)
        
    def update(self, H, P_hat, X_hat, R, Z):
        #print(P_hat, H.transpose(), H)
        K = np.dot(np.dot(P_hat, H.transpose()), np.linalg.inv(np.dot(np.dot(H, P_hat), H.transpose()) + R))
        X = X_hat + np.dot(K, Z-self.h(X_hat))
        X[6, 0] = X[6, 0] % 360
        P = np.dot(np.eye(8) - np.dot(K, H), P_hat)
        return (K, X, P)
        
    def h(self, X):
        return np.array([[X[2, 0] * cos(X[6, 0]) + X[5, 0] * sin(X[6, 0])],
                         [X[5, 0] * cos(X[6, 0]) - X[2, 0] * sin(X[6, 0])],
                         [X[1, 0] * cos(X[6, 0]) + X[4, 0] * sin(X[6, 0])],
                         [X[4, 0] * cos(X[6, 0]) - X[1, 0] * sin(X[6, 0])],
                         [X[7, 0]],
                         [X[7, 0]]])
        
    def compute_H(self, X):
        return np.array([[0, cos(X[6, 0]), 0, 0, sin(X[6, 0]), 0, - X[1, 0] * sin(X[6, 0]) + X[4, 0] * cos(X[6, 0]), 0],
                      [0, -sin(X[6, 0]), 0, 0, cos(X[6, 0]), 0, - X[4, 0] * sin(X[6, 0]) - X[1, 0] * cos(X[6, 0]), 0],
                      [0, 0, cos(X[6, 0]), 0, 0, sin(X[6, 0]), - X[2, 0] * sin(X[6, 0]) + X[5, 0] * cos(X[6, 0]), 0],
                      [0, 0, -sin(X[6, 0]), 0, 0, cos(X[6, 0]), - X[5, 0] * sin(X[6, 0]) - X[2, 0] * cos(X[6, 0]), 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1]])#,
                      #[cos(theta), 0, 0, sin(theta), 0, 0, - N * sin(theta) - E * cos(theta), 0],
                      #[-sin(theta), 0, 0, 0, cos(theta), 0, - E * sin(theta) + N * cos(theta), 0]])

    def Set_NFC(X):
        pass
        #(X[0, 0], X[2, 0]) = Get_Loc_from_Dot(point, position)

    def compute_Y(self, X):
        return np.dot(np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 1, 0]]), X)
        
    def run(self): 
        posX = []
        vitX = []
        accX = []
        posY = []
        vitY = []
        accY = []
        posTheta = []
        vitTheta = []
        posXhat = []
        posYhat = []
        posThetahat = []
        
        AccX = []
        AccY = []
        GyrZ = []
        OdoX = []
        OdoY = []
        OdoZ = []
        
        
        dt = 0.2
        counter = 0
        (A, X, R, Q, P) = self.initialize(0, 0, 0, 0, 0, 0, 0, 0, dt, 0.1, 3*10**(-5), 0.1, 0, 0, 0, 0, 0)
        print(A, X, R, Q, P)
        while not self.interrupt:
        #with open('./EKF/North_3m05_11s69.txt') as f:
        #    lines = f.readlines()
        #    f.close()
            (X_hat, P_hat) = self.predict(X, A, P, Q)
            t = time()
            Z_hat = self.measurement()
        #for i in lines:
        #    (X_hat, P_hat) = self.predict(X, A, P, Q)
        #    print("X_hat", X_hat)
        #    posXhat.append(X_hat[0, 0])
        #    posYhat.append(X_hat[3, 0])
        #    posThetahat.append(X_hat[6, 0])
        #    #print(X_hat, P_hat)
        #    Z = self.measurement(i)
        #    AccX.append(Z[2, 0]) 
        #    AccY.append(Z[3, 0])
        #    GyrZ.append(Z[4, 0])
        #    OdoX.append(Z[0, 0])
        #    OdoY.append(Z[1, 0])
        #    OdoZ.append(Z[5, 0])
            
            
            #print(Z)
            H = self.compute_H(X)
            #print(Z)
            try:
                (K, X, P) = self.update(H, P_hat, X_hat, R, Z)
            except:
                error = 1
            if self.NFC_Alert:
                X = self.Set_NFC(X)
                
            Y = self.compute_Y(X)

            coordinate.Write_Loc(Y[0, 0], Y[1, 0], Y[2, 0])
            counter += 1        
            #print("X", X)
            #print(K, X, P)
            
            #posX.append(X[0, 0])
            #vitX.append(X[1, 0])
            #accX.append(X[2, 0])
            #posY.append(X[3, 0])
            #vitY.append(X[4, 0])
            #accY.append(X[5, 0])
            #posTheta.append(X[6, 0])
            #vitTheta.append(X[7, 0])
            #print("X = ", X[0, 0])
            #print("Y = ", X[3, 0])
            #print("Theta = ", X[6, 0])
            #counter += 1
            #print(counter)
            
        #plt.plot(range(counter), accY)
        #plt.plot(range(counter), posTheta)
        #print(posX)
        #print("AccX: ", AccX)
        #print("AccY: ", AccY)
        #print("OdoX: ", OdoX)
        #print("OdoY: ", OdoY)
        #print("OdoZ: ", OdoZ)
        #print("GyrX: ", GyrZ)
        #plt.plot(range(10), posTheta)
        #print (posX, posY)
        #print(posX, posY, posTheta)
        #plt.plot(posY, range(100))
        #plt.plot(posTheta, range(100))
        return 0
thread_localisation = Filter()    
if __name__ == '__main__':
    ekf = Filter()
    
    ekf.run()

    print("END")
    