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
    def initialize(self, x, y, z, vx, vy, vz, ax, ay, dt, Sigma_odom, Sigma_acc, Sigma_gyro, err_N, err_N_dot, err_N_dot_dot, err_E, err_E_dot, err_E_dot_dot, err_theta, err_theta_dot):
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
       
        Q = np.array([[err_N, 0, 0, 0, 0, 0, 0, 0],
                     [0, err_N_dot, 0, 0, 0, 0, 0, 0],
                     [0, 0, err_N_dot_dot, 0, 0, 0, 0, 0],
                     [0, 0, 0, err_E, 0, 0, 0, 0],
                     [0, 0, 0, 0, err_E_dot, 0, 0, 0],
                     [0, 0, 0, 0, 0, err_E_dot_dot, 0, 0],
                     [0, 0, 0, 0, 0, 0, err_theta, 0],
                     [0, 0, 0, 0, 0, 0, 0, err_theta_dot]])
        
        P = np.eye(8)*0.405
        
        return (A, X, R, Q, P)
    
    def measurement(self, line):
        words = line.split()
        ax = 0#float(words[1])*0.01
        ay = 0#float(words[0])*0.01
        theta_dotGz = 0#2*np.pi/360*float(words[4])
        vx = float(words[2])*0.89
        vy = float(words[3])*0.89
        theta_dotOz = float(words[5])*0.63

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
        
        
        dt = 0.1
        counter = 0
        (A, X, R, Q, P) = self.initialize(0, 0, 0, 0, 0, 0, 0, 0, dt, 0.1, 3*10**(-5), 0.1, 0, 0, 0, 0, 0, 0, 0, 0)
        print(A, X, R, Q, P)
        #while true()
        with open('./EKF/Forward.txt') as f:
            lines = f.readlines()
            f.close()

        for i in lines:
            (X_hat, P_hat) = self.predict(X, A, P, Q)
            print("X_hat", X_hat)
            posXhat.append(X_hat[0, 0])
            posYhat.append(X_hat[3, 0])
            posThetahat.append(X_hat[6, 0])
            #print(X_hat, P_hat)
            Z = self.measurement(i)
            AccX.append(Z[2, 0]) 
            AccY.append(Z[3, 0])
            GyrZ.append(Z[4, 0])
            OdoX.append(Z[0, 0])
            OdoY.append(Z[1, 0])
            OdoZ.append(Z[5, 0])
            
            
            print(Z)
            H = self.compute_H(X)
            #print(Z)
            try:
                (K, X, P) = self.update(H, P_hat, X_hat, R, Z)
            except:
                error = 1
                
            print("X", X)
            #print(K, X, P)
            
            posX.append(X[0, 0])
            vitX.append(X[1, 0])
            accX.append(X[2, 0])
            posY.append(X[3, 0])
            vitY.append(X[4, 0])
            accY.append(X[5, 0])
            posTheta.append(X[6, 0])
            vitTheta.append(X[7, 0])
            #print("X = ", X[0, 0])
            #print("Y = ", X[3, 0])
            #print("Theta = ", X[6, 0])
            counter += 1
            print(counter)
        
        plt.plot(posY, posX)
        
        #plt.plot(range(counter), posYhat) # 4
        #plt.plot(range(counter), vitX) # 6*10**(-3)
        #plt.plot(range(counter), accX) # 1*10**(-3)
        #plt.plot(range(counter), posY) # -1.3*10**(-3)
        #plt.plot(range(counter), vitY) # 2*10**(-4)
        #plt.plot(range(counter), accY) # 2*10**(-5)
        #plt.plot(range(counter), posTheta) # 4.33*10**(-6)
        #plt.plot(range(counter), vitTheta) # 3.73*10**(-5)
        

        #print(posYhat)
        #print("AccX: ", AccX)
        #print("AccY: ", AccY)
        #print("OdoX: ", OdoX)
        #print("OdoY: ", OdoY)
        #print("OdoZ: ", OdoZ)
        #print("GyrX: ", GyrZ)

        return 0
    
if __name__ == '__main__':
    ekf = EKF()
    
    ekf.run()

    print("END")
    