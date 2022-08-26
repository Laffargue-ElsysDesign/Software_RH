# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import time
#from holo32.holo_uart_management import odometry

"""
Created on Mon Jun 27 08:32:09 2022

@author: laffargue
"""

def cos(a):
    return np.cos(a*np.pi/180)

def sin(a):
    return np.sin(a*np.pi/180)

class EKF():
    def initialize(self, x, y, z, vx, vy, vz, ax, ay, dt, Sigma_odom, Sigma_gyro, err_N_dot, err_E_dot, err_theta_dot):
        A = np.array([[1, dt, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 0],
                     [0, 0, 1, dt, 0, 0],
                     [0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 1, dt],
                     [0, 0, 0, 0, 0, 1]])
        
        X = np.array([[x],
                      [vx],
                      [y], 
                      [vy], 
                      [z],
                      [vz]])
        
        R = np.array([[Sigma_odom, 0, 0, 0],
                     [0, Sigma_odom, 0, 0],
                     [0, 0, Sigma_odom, 0],
                     [0, 0, 0, Sigma_gyro]])
       
        Q = np.array([[0, 0, 0, 0, 0, 0],
                     [0, err_N_dot, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, err_E_dot, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, err_theta_dot]])
        
        P = np.eye(6)*1
        
        return (A, X, R, Q, P)
    
    def measurement(self, line):
        words = line.split()
        theta_dotGz = 0#2*np.pi/360*float(words[5])
        vx = int(words[1])*0.89
        vy = int(words[0])*0.89
        theta_dotOz = 0#float(words[2])*3

        return np.array([[vx], [vy], [theta_dotOz], [theta_dotGz]])
    
    def predict(self, X, A, P, Q):
        X_hat = np.dot(A, X)
        X_hat[4, 0] = X_hat[4, 0] % 360
        P_hat = np.dot(np.dot(A, P), A.transpose()) + Q
        return (X_hat, P_hat)
        
    def update(self, H, P_hat, X_hat, R, Z):
        #print(P_hat, H.transpose(), H)
        K = np.dot(np.dot(P_hat, H.transpose()), np.linalg.inv(np.dot(np.dot(H, P_hat), H.transpose()) + R))
        print("K: ", K)
        print("h: ", self.h(X_hat))
        X = X_hat + np.dot(K, Z-self.h(X_hat))
        X[4, 0] = X[4, 0] % 360
        P = np.dot(np.eye(6) - np.dot(K, H), P_hat)
        return (K, X, P)
        
    def h(self, X):
        return np.array([[X[1, 0] * cos(X[4, 0]) + X[3, 0] * sin(X[4, 0])],
                         [X[3, 0] * cos(X[4, 0]) - X[1, 0] * sin(X[4, 0])],
                         [X[5, 0]],
                         [X[5, 0]]])
        
    def compute_H(self, X):
        return np.array([[0, cos(X[4, 0]), 0, sin(X[4, 0]), - X[1, 0] * sin(X[4, 0]) + X[4, 0] * cos(X[4, 0]), 0],
                      [0, -sin(X[4, 0]), 0, cos(X[4, 0]), - X[4, 0] * sin(X[4, 0]) - X[1, 0] * cos(X[4, 0]), 0],
                      [0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 1]])
        
        
    def run(self): 
        posX = []
        posY = []
        posTheta = []
        posXhat = []
        posYhat = []
        posThetahat = []
        
        GyrZ = []
        OdoX = []
        OdoY = []
        OdoZ = []
        
        
        dt = 0.2
        counter = 0
        (A, X, R, Q, P) = self.initialize(0, 0, 0, 0, 0, 0, 0, 0, dt, 0.1, 0.1, 0.1, 0.1, 0.1)
        print(A, X, R, Q, P)
        #while true()
        with open('EKF/odometryNorth.txt') as f:
            lines = f.readlines()
            f.close()

        for i in lines:
            (X_hat, P_hat) = self.predict(X, A, P, Q)
            print("X_hat", X_hat)
            posXhat.append(X_hat[0, 0])
            posYhat.append(X_hat[2, 0])
            posThetahat.append(X_hat[4, 0])
            #print(X_hat, P_hat)
            Z = self.measurement(i)
            GyrZ.append(Z[2, 0])
            OdoX.append(Z[0, 0])
            OdoY.append(Z[1, 0])
            OdoZ.append(Z[3, 0])
            
            
            print("Z : ", Z)
            H = self.compute_H(X)
            #print(Z)
            #try:
            (K, X, P) = self.update(H, P_hat, X_hat, R, Z)
            #except:
            #    error = 1
                
            print("X: ", P)
            #print(K, X, P)
            
            posX.append(X[0, 0])
            posY.append(X[2, 0])
            posTheta.append(X[4, 0])

            counter += 1
            print(counter)
            #if counter == 10:
                #break
            
        plt.plot(posX, posY)

        print("posX: ", posX)
        print("OdoX: ", OdoX)
        print("OdoY: ", OdoY)
        print("OdoZ: ", OdoZ)
        print("GyrZ: ", GyrZ)

        return 0
    
if __name__ == '__main__':
    ekf = EKF()
    
    ekf.run()

    print("END")
    