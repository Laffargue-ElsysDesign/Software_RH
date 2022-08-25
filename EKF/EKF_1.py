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
    
    def measurement(self, line):
        words = line.split()
        
        vx = int(words[10])*0.89
        vy = int(words[9])*0.89
        vz = int(words[11])*0.41

        return np.array([[vx], [vy], [vz]])
        
    def compute_X(self, X, Z):
        return np.dot(self.A, X) + np.dot(self.B, Z)
    
    def compute_Y(self, X):
        return np.dot(self.C, X)
    
    def change_orthogonal(self, X, Z_hat):
        G = np.array([[cos(X[4, 0]), -sin(X[4, 0]), 0],
                      [sin(X[4, 0]), cos(X[4, 0]), 0],
                      [0, 0, 1]])
        print("G: ", G)
        
        return np.dot(G, Z_hat)
        
        
    def run(self): 
        posX = []
        posY = []
        posTheta = []
        
        OdoX = []
        OdoY = []
        OdoZ = []
        
        
        dt = 0.113
        counter = 0
        X = self.initialize(0, 0, 0, 0, 0, 0, dt)
        #print(A, B, C, X)
        
        #while true()
        
        with open('EKF/North_3m05_11s69.txt') as f:
            lines = f.readlines()
            f.close()

        for i in lines:
            
            Z_hat = self.measurement(i)
            
            print("Z_hat : ", Z_hat)
            
            Z = self.change_orthogonal(X, Z_hat)
            
            print("Z: ", Z)

            OdoX.append(Z_hat[0, 0])
            OdoY.append(Z_hat[1, 0])
            OdoZ.append(Z_hat[2, 0])
            
            X = self.compute_X(X, Z)
                
            print("X", X)
            
            Y = self.compute_Y(X)
            posX.append(Y[0, 0])
            posY.append(Y[1, 0])
            posTheta.append(Y[2, 0])

            counter += 1
            #print(counter)
            #if counter == 161:
            #    break
            
        plt.plot(posX, posY)
        #plt.plot(range(counter), posTheta)
        print("posX : ", posX)
        print("posY : ", posY)
        print("posTheta : ", posTheta)

        print("OdoX: ", OdoX)
        print("OdoY: ", OdoY)
        print("OdoZ: ", OdoZ)

        return 0
    
if __name__ == '__main__':
    ekf = EKF()
    
    ekf.run()

    print("END")
    