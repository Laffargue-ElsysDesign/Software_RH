# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import time

"""
Created on Mon Jun 27 08:32:09 2022

@author: laffargue
"""

def cos(a):
    return np.cos(a*np.pi/180)

def sin(a):
    return np.sin(a*np.pi/180)

class EKF():
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
        
        R = np.array([[Sigma_odom, 0, 0, 0, 0, 0],# 0, 0],
                     [0, Sigma_odom, 0, 0, 0, 0],# 0, 0],
                     [0, 0, Sigma_acc, 0, 0, 0],# 0, 0],
                     [0, 0, 0, Sigma_acc, 0, 0],# 0, 0],
                     [0, 0, 0, 0, Sigma_odom, 0],# 0, 0],
                     [0, 0, 0, 0, 0, Sigma_gyro]])#, 0, 0],
                     #[0, 0, 0, 0, 0, 0, Sigma_odom, 0],
                     #[0, 0, 0, 0, 0, 0, 0, Sigma_odom]])
       
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
        ax = 1
        ay = 0
        #dx = 0
        #dy = 0
        vx = 0
        vy = 0
        theta_dotOz = 36
        theta_dotGz = 36
        return np.array([[vx], [vy], [ax], [ay], [theta_dotOz], [theta_dotGz]])#, [dx], [dy]])
    
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
                         [X[7, 0]]])#,
                         #[X[0, 0] * cos(X[6, 0]) + X[3, 0] * sin(X[6, 0])],
                         #[X[3, 0] * cos(X[6, 0]) - X[0, 0] * sin(X[6, 0])]])
        
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
        posY = []
        posTheta = []
        posXhat = []
        posYhat = []
        posThetahat = []
        dt = 1
        (A, X, R, Q, P) = self.initialize(0, 0, 0, 0, 0, 36, 1, 0, dt, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
        print(A, X, R, Q, P)
        #while true()
        for i in range(100):
            (X_hat, P_hat) = self.predict(X, A, P, Q)
            print("X_hat", X_hat)
            posXhat.append(X_hat[0, 0])
            posYhat.append(X_hat[3, 0])
            posThetahat.append(X_hat[6, 0])
            #print(X_hat, P_hat)
            Z = self.measurement()
            H = self.compute_H(X)
            #print(Z)
            (K, X, P) = self.update(H, P_hat, X_hat, R, Z)
            print("X", X)
            #print(K, X, P)
            
            posX.append(X[0, 0])
            posY.append(X[3, 0])
            posTheta.append(X[6, 0])
            #print("X = ", X[0, 0])
            #print("Y = ", X[3, 0])
            #print("Theta = ", X[6, 0])
            
        plt.plot(posX, posY)
        #plt.plot(range(10), posTheta)
        #print (posX, posY)
        #print(posX, posY, posTheta)
        #plt.plot(posY, range(100))
        #plt.plot(posTheta, range(100))
        return 0
    
if __name__ == '__main__':
    ekf = EKF()
    
    ekf.run()
    #print(cos(450))
    #test = np.array([[1, 2],
                     #[3, 4]])
    #print(test)
    #print(np.linalg.inv(np.dot(np.transpose(test), test)))
    print("END")
    