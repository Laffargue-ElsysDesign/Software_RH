# -*- coding: utf-8 -*-
from threading import Thread, Lock
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

    def initialize(self, x, y, z, vx, vy, vz, dt):
        self.A = np.array([[1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0]])
        
        self.B = np.array([[dt, 0, 0],
                     [1, 0, 0, ],
                     [0, dt, 0],
                     [0, 1, 0],
                     [0, 0, dt],
                     [0, 0, 1]])
        
        self.C = np.array([[1, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0]])
        
        
        X = np.array([[x],
                      [vx],
                      [y], 
                      [vy],  
                      [z],
                      [vz]])
       
        
        return X
    
    def measurement(self):
        R_vx, R_vy, R_vz = odometry.Read()
        R_ax, R_ay, R_gz = imu_data.Read()
        
        vx = R_vx*0.89
        vy = R_vy*0.89
        vz = R_vz*0.62
        #print(R_vx, R_vy, R_ax, R_ay, R_gz, R_vz)
        return np.array([[vx], [vy], [vz]])
        
    def compute_X(self, X, Z):
        return np.dot(self.A, X) + np.dot(self.B, Z)
    
    def compute_Y(self, X):
        return np.dot(self.C, X)
    
    def change_orthogonal(self, X, Z_hat):
        G = np.array([[cos(X[4, 0]), -sin(X[4, 0]), 0],
                      [sin(X[4, 0]), cos(X[4, 0]), 0],
                      [0, 0, 1]])
        #print("G: ", G)
        
        return np.dot(G, Z_hat)
        
    def Set_NFC(X):
        pass
        #(X[0, 0], X[2, 0]) = Get_Loc_from_Dot(point, position)
        
    def run(self):     
        dt = 0.15
        counter = 0
        X = self.initialize(0, 0, 180, 0, 0, 0, dt)
        #print(A, B, C, X)
        
        while not self.interrupt:
        
        #with open('EKF/North_3m05_11s69.txt') as f:
        #    lines = f.readlines()
        #    f.close()
        #for i in lines:
            t=time()
            Z_hat = self.measurement()
            
            #print("Z_hat : ", Z_hat)
            
            Z = self.change_orthogonal(X, Z_hat)
            
            #print("Z: ", Z)

            #OdoX.append(Z_hat[0, 0])
            #OdoY.append(Z_hat[1, 0])
            #OdoZ.append(Z_hat[2, 0])
            
            X = self.compute_X(X, Z)

            #Angle modulo 360 pour garde run intervaller entre 0 et 360 (j'ai pas trouvé mieux comme calcul)
            X[2, 0] = X[2, 0] % 360    
            #print("X", X)
            if self.NFC_Alert:
                X = self.Set_NFC(X)
            
            Y = self.compute_Y(X)
            #print(Y[0, 0], Y[1, 0], Y[2, 0])
            coordinate.Write_Loc(Y[0, 0], Y[1, 0], Y[2, 0])
            #posX.append(Y[0, 0])
            #posY.append(Y[1, 0])
            #posTheta.append(Y[2, 0])

            counter += 1
            #if counter == 161:
            #    break
            while time()<t+dt:
                sleep(0.001)
        #plt.plot(posX, posY)
        #plt.plot(range(counter), posTheta)
        #print("posX : ", posX)
        #print("posY : ", posY)
        #print("posTheta : ", posTheta)

        #print("OdoX: ", OdoX)
        #print("OdoY: ", OdoY)
        #print("OdoZ: ", OdoZ)

        return 0

thread_localisation = Filter()
    
if __name__ == '__main__':
    ekf = Filter()
    
    ekf.run()

    print("END")
    