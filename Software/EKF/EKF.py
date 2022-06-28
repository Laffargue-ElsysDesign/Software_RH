# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import time

"""
Created on Mon Jun 27 08:32:09 2022

@author: laffargue
"""


class EKF():
    def initialize(self, dt, Sigma_odom, Sigma_acc, Sigma_gyro, err_N_dot, err_N_dot_dot, err_E_dot, err_E_dot_dot, err_theta_dot):
        delta_T = dt
        A = np.array([[1, delta_T, (delta_T**2)/2, 0, 0, 0, 0, 0],
                     [0, 1, delta_T, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0],
                     [0 ,0 ,0 ,1 , delta_T, (delta_T*2)/2, 0, 0],
                     [0, 0, 0, 0, 1, delta_T, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, delta_T],
                     [0, 0, 0, 0, 0, 0, 0, 1]])
        
        X = np.array([[5],
                      [0],
                      [0],
                      [4], 
                      [0], 
                      [0], 
                      [0],
                      [0]])
       
        H = self.compute_H(X[0, 0], X[3, 0], X[1, 0], X[4, 0], X[6, 0])
        print(H)
        
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
        
        return (A, X, H, R, Q, P)
    
    def measurement(self):
        ax = 0
        ay = 0
        dx = 0
        dy = 0
        vx = 0
        vy = 0
        theta = 0
        theta_dot = 0
        return np.array([[ax], [ay], [vx], [vy], [theta], [theta_dot]])#, [dx], [dy]])
    
    def predict(self, X, A, P, Q):
        X_hat = np.dot(A, X)
        P_hat = np.dot(np.dot(A, P), A.transpose()) + Q
        return (X_hat, P_hat)
        
    def update(self, H, P_hat, X_hat, R, Z):
        print(P_hat, H.transpose(), H)
        K = np.dot(np.dot(P_hat, H.transpose()), np.linalg.inv(np.dot(np.dot(H, P_hat), H.transpose()) + R))
        X = X_hat + np.dot(K, Z-self.h(X_hat))
        P = np.dot(np.eye(8) - np.dot(K, H), P_hat)
        return (K, X, P)
        
    def h(self, X):
        return np.array([[X[2, 0] * np.cos(X[6, 0]) + X[5, 0] * np.sin(X[6, 0])],
                         [X[5, 0] * np.cos(X[6, 0]) - X[2, 0] * np.sin(X[6, 0])],
                         [X[1, 0] * np.cos(X[6, 0]) + X[4, 0] * np.sin(X[6, 0])],
                         [X[4, 0] * np.cos(X[6, 0]) - X[1, 0] * np.sin(X[6, 0])],
                         [X[7, 0]],
                         [X[7, 0]]])#,
                         #[X[0, 0] * np.cos(X[6, 0]) + X[3, 0] * np.sin(X[6, 0])],
                         #[X[3, 0] * np.cos(X[6, 0]) - X[0, 0] * np.sin(X[6, 0])]])
        
    def compute_H(self, N, E, N_dot, E_dot, theta):
        return np.array([[0, np.cos(theta), 0, 0, np.sin(theta), 0, - N_dot * np.sin(theta) - E_dot * np.cos(theta), 0],
                      [0, -np.sin(theta), 0, 0, np.cos(theta), 0, - E_dot * np.sin(theta) + N_dot * np.cos(theta), 0],
                      [0, 0, np.cos(theta), 0, np.sin(theta), 0, - N_dot * np.sin(theta) - E_dot * np.cos(theta), 0],
                      [0, 0, -np.sin(theta), 0, np.sin(theta), 0, - E_dot * np.sin(theta) + N_dot * np.cos(theta), 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1]])#,
                      #[np.cos(theta), 0, 0, np.sin(theta), 0, 0, - N * np.sin(theta) - E * np.cos(theta), 0],
                      #[-np.sin(theta), 0, 0, 0, np.cos(theta), 0, - E * np.sin(theta) + N * np.cos(theta), 0]])
        
        
    def run(self): 
        posX = []
        posY = []
        posTheta = []
        dt = 0.01
        (A, X, H, R, Q, P) = self.initialize(dt, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
       # print(A, X, H, R, Q, P)
        #while true()
        for i in range(100):
            (X_hat, P_hat) = self.predict(X, A, P, Q)
            #print(X_hat, P_hat)
            Z = self.measurement()
            #print(Z)
            (K, X, P) = self.update(H, P_hat, X_hat, R, Z)
            #print(K, X, P)
            posX.append(X[0, 0])
            posY.append(X[3, 0])
            posTheta.append(X[6, 0])
            print("X = ", X[0, 0])
            print("Y = ", X[3, 0])
            print("Theta = ", X[6, 0])
            
        plt.plot(posX, range(100))
        plt.plot(posY, range(100))
        plt.plot(posTheta, range(100))
        return 0
    
if __name__ == '__main__':
    ekf = EKF()
    
    ekf.run()
    #test = np.array([[1, 2],
                     #[3, 4]])
    #print(test)
    #print(np.linalg.inv(np.dot(np.transpose(test), test)))
    print("END")
    