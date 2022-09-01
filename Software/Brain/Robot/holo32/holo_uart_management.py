#====Classic import====#
import numpy as np
import math
import sys
from sys import exit
from time import sleep, time
#from math import sin, cos, pi
from threading import Thread, Lock
from signal import signal, SIGINT

#=====PYNQ import=====#
from pynq import Overlay

class Class_Command:
    def __init__(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.MUT = Lock()

    def Set_Speed(self, x, y, z):
        self.MUT.acquire()
        self.speed_x = x
        self.speed_y = y
        self.speed_z = z
        self.MUT.release()

    def Get_Trajectory(self, read_input):
        if read_input==' ':
            print("Stop")
            self.Set_Speed(0, 0, 0)

        elif read_input=='z':
            print("Avance")
            self.Set_Speed(0.3, 0, 0)

        elif read_input=='d':
            print("Droite")
            self.Set_Speed(0, 0.3, 0)

        elif read_input=='q':
            print("Gauche")
            self.Set_Speed(0, -0.3, 0)

        elif read_input=='s':
            print("Arriere")
            self.Set_Speed(-0.3, 0, 0)

        elif read_input=='e':
            print("Nord-est")
            self.Set_Speed(0.3, 0.3, 0)

        elif read_input=='a':
            print("Nord-ouest")
            self.Set_Speed(0.3, -0.3, 0)

        elif read_input=='w':
            print("Sud-ouest")
            self.Set_Speed(-0.3, 0.3, 0)

        elif read_input=='x':
            print("sud-est")
            self.Set_Speed(-0.3, -0.3, 0)

        elif read_input=='"':
            print("pivot droite")
            self.Set_Speed(0, 0, 0.3)

        elif read_input=='é':
            print("pivot gauche")
            self.Set_Speed(0, 0, -0.3)
            
        else:
            print("Input error, please retry")
        return 1  

class Class_Odom:
    def __init__(self):
        self.stack = []
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.dist_x = 0
        self.dist_y = 0
        self.ang_z = 0
        self.MUT = Lock()
        
    def Read(self):
        self.MUT.acquire()
        Sx = self.speed_x
        Sy = self.speed_y
        Sz = self.speed_z
        self.MUT.release()
        return Sx, Sy, Sz

cmd_robot = Class_Command()
odometry = Class_Odom()

#=================fonctions===============

#complement a deux 
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val    

#lecture de l'uart via IP FPGA et librairie custom
def readTrame_uart(uart): 
    buf=[]
    try: 
        buf=uart.readMessage(90,165,16,100,timeout=0.5) #custom librairie, arg: SOF, EOF, TAILLE, nbr de tentative, timeout
    except:
        #print ("uart silencieuse")
        return False
    
    #print ("uart recu")

    #=======debug=======
        #print("receive")
        #print(*buf, sep = ", ")
        #print(time())
        #print(buf[5])
        #print("6=")
        #print("6t=",twos_comp((buf[6]),8),"8t=",twos_comp((buf[8]),8),"10t=",twos_comp((buf[10]),8))
    #print(buf)
    global odometry
    odometry.MUT.acquire()

    odometry.speed_x=twos_comp((buf[-10]),8)
    odometry.speed_y=-twos_comp((buf[-8]),8)
    odometry.speed_z=twos_comp((buf[-6]),8)
    odometry.ang_z=twos_comp(buf[-3],8)
    odometry.dist_y=twos_comp(buf[-4],8)
    odometry.dist_x=twos_comp(buf[-5],8)
    odometry.stack.append(odometry.speed_z)
    
    odometry.MUT.release()
    return True

class Holo_UART(Thread):
    def __init__(self, overlay):
        Thread.__init__(self)
        
        self.uart = overlay.axi_uartlite_0 
        
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.msg= [0x5A, 0x00, 0x00,  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0xA5] 

    

    def run(self):
        
        while True :

            global cmd_robot
            cmd_robot.MUT.acquire()
           
            self.speed_x = cmd_robot.speed_x*100
            self.speed_y = cmd_robot.speed_y*100
            self.speed_z = cmd_robot.speed_z*100
            cmd_robot.MUT.release()
            if (self.speed_x < 0):
                self.speed_x = self.speed_x+255 #uart non signe, reception signe
            else:
                self.speed_x = self.speed_x

            if (self.speed_z < 0):
                self.speed_z = self.speed_z+255 #uart non signe, reception signe
            else:
                self.speed_z = self.speed_z
                
            if (self.speed_y < 0):
                self.speed_y = self.speed_y+255 #uart non signe, reception signe
            else:
                self.speed_y = self.speed_y


            
            if (not math.isnan(self.speed_x)):
                self.msg[5] = int(self.speed_x)
                
            if (not math.isnan(self.speed_y)):
                self.msg[6] = int(self.speed_y)
                
            if (not math.isnan(self.speed_z)):
                self.msg[7] = int(self.speed_z)            
            
            try:
                #I = input("Enter")
                #print(self.msg)
                self.uart.writeByte(self.msg) 
            except:
                print("Send timeout")
                
            readTrame_uart(self.uart)
            #print(odometry.speed_x, " ", odometry.speed_y, " ", odometry.speed_z)
            sleep(0.05)

def init():
    duree_tour=6.5 #duree d'un tour en seconde 
    #duree_ecoute_acc=2
    debut_init = time()
    #print("<===========init mag============>")
    #global msg_mag
    #mag_lock.acquire()
    #max_x=msg_mag[0]
    #min_x=msg_mag[0]
    #max_y=msg_mag[1]
    #min_y=msg_mag[1]
    #mag_lock.release()
    
    #global msg_acc
    #global Z_GYRO_OFFSET
    #global X_ACC_OFFSET
    #global Y_ACC_OFFSET
    #buf_gyro = []
    
    global cmd_robot
    cmd_robot.MUT.acquire()
    cmd_robot.speed_z = 0.5
    cmd_robot.MUT.release()
    sleep(0.5)
    cmd_robot.MUT.acquire()
    cmd_robot.speed_z = 1
    cmd_robot.MUT.release()
    #while time()<debut_init+duree_tour:
        #mag_lock.acquire()
        #tmp_x=msg_mag[0]*1000000
        #tmp_y=msg_mag[1]*1000000
        #mag_lock.release()
        #if max_x<tmp_x:
            #max_x=tmp_x
        #if min_x>tmp_x:
            #min_x=tmp_x
        #if max_y<tmp_y:
           # max_y=tmp_y
        #if min_y>tmp_y:
            #min_y=tmp_y
    cmd_robot.MUT.acquire()
    cmd_robot.speed_z = 0
    cmd_robot.MUT.release()    
    #global X_MAG_OFFSET
    #X_MAG_OFFSET = (max_x-min_x)/2-max_x
    #global Y_MAG_OFFSET
    #Y_MAG_OFFSET = (max_y-min_y)/2-max_y
    ##print("<===========init mag done============>")
    ##print("max_x: ",max_x,"; min_x: ",min_x,"max_y: ",max_y,"; min_y: ",min_y,)
    #print("XMAGOFFSET=",X_MAG_OFFSET,"; YMAGOFFSET=",Y_MAG_OFFSET)
    #sleep(2)
    #debut_init = time()
    #while time()<debut_init+duree_ecoute_acc:
        #acc_lock.acquire()
        #buf_gyro.append(msg_acc[5])
        #acc_lock.release()
        
    #acc_lock.acquire()
    #X_ACC_OFFSET = msg_acc[0]
    #Y_ACC_OFFSET = msg_acc[1]
    #acc_lock.release()
    #Z_GYRO_OFFSET = np.mean(buf_gyro) 
    #print("<===========init acc done============>")
    #print("X_ACC_OFFSET=",X_ACC_OFFSET,"; Y_ACC_OFFSET=",Y_ACC_OFFSET,"; Z_GYRO_OFFSET=",Z_GYRO_OFFSET)
    
    global init_done
    init_done=True


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

if __name__ == '__main__':
    
    signal(SIGINT, handler)

    global overlay
    overlay=Overlay("./Overlays/Bitstream/UartComm.bit", download=False)
    if overlay.is_loaded()==False:
        print("Loading Overlay ...")
        overlay.download()
    
    print('Bring up uart....')
    
    thread_holo = Holo_UART()
    thread_holo.start()
   
    ##thread_imu = IMU_I2C()
    ##thread_imu.start()

    ##ros_talker = MyTalker()
    ##ros_talker.start()
    
    ##init()
