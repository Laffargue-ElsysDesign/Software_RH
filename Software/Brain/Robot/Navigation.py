from operator import truediv
from threading import Thread, Lock
from time import sleep, time
from Robot.EKF import coordinate
from Robot.Localisation import Get_Orientation
from numpy import mgrid
from Robot.Alerts import Mgt
import Robot.Localisation as Loc
from Robot.Alerts import alerts
import numpy as np
from Robot.Evitement import raw_command

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Navigation Exiting gracefully')
    exit(0)

def Dijkstra(End):
    pass #TBD

def Compute_Angle(end_angle):
    angle = end_angle - coordinate.Get_Angle()

    if np.abs(angle) > 180:
        angle = 360 - np.abs(angle)

    return angle
    

def Robot_Rotate(Turn_Right):
    
    print("Rotate")
    if Turn_Right:
        raw_command.Set(0, 0, 0.1)
    else:
        raw_command.Set(0, 0, -0.1) 
    return 1

def Robot_Stop():
    print("Stop")
    raw_command.Set(0, 0, 0)
    return 1
        

def Robot_Forward():
    raw_command.Set(0.2, 0, 0)
    return 1

def Procedure():
    pass #TBD:  Routine when ariving on a point

class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = [0, 0] #TBD
        self.mgt = Mgt()
        self.MUT = Lock()
        self.interrupt = False

    def Set_Path(self, path):
        self.MUT.acquire()
        self.path = path
        self.MUT.release()

    def Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()
    
    def Check_NFC(self, point, old_point):
        output = False
        if alerts.Get_NFC_Alert():
            Robot_Stop()
            sleep(0.5)
            output = False
            data_valid, tag_point, tag_position = alerts.Get_NFC_Tag()
            if data_valid and tag_point == point:
                #print("point reached")
                output = True
            elif data_valid:
                #print("interrupting", point, old_point, tag)
                self.mgt.Stop()
                output = True
            alerts.Reset_Tag_Alert()
        return output

    def Orientation(self, point, old_point):
        angle_wanted = Get_Orientation(old_point, point)
        angle = Compute_Angle(angle_wanted)

        while ((not np.abs(angle) < 2) and (not self.mgt.Check_Stop())):
            print(angle)
            Turn_Right = True
            #print(angle, np.abs(angle))
            if angle < 0:
                Turn_Right = False
            
            Robot_Rotate(Turn_Right)

            angle = Compute_Angle(angle_wanted)

        Robot_Stop()


    def Get_to_Point(self, point, old_point):
        if point == old_point:
            return 
            #End = Check_NFC(self.path, point, old_point)
        else:

            self.Orientation(point, old_point)

            if self.mgt.Check_Stop():
                return
            
            Robot_Forward()
            alerts.Reset_Tag_Alert()

            while not self.Check_NFC(point, old_point) and not self.interrupt:
                Robot_Forward()
            
            Robot_Forward()
            sleep(0.7)
            Robot_Stop()

            if self.mgt.Check_Stop():
                return
    

    def Wait_Start(self):
        print("End of navigation")
        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
        self.mgt.Is_Not_Waiting()
        return

    def run(self):
        while not self.interrupt:
            self.Wait_Start()
            print("Start of Navigation")
            #T = time()
            #print("path:", self.path)
            while not self.mgt.Check_Stop() and not self.interrupt:
                #sleep(1)
                #if time() > (T + 10):
                    #self.mgt.Stop()
                old_point = self.path[0]
                for i in self.path:
                    print("Going to ", i)
                    self.Get_to_Point(i, old_point)
                    if self.mgt.Check_Stop() or self.interrupt:
                        print("interupted")
                        break
                    old_point = i
                self.mgt.Stop()
                #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    #Procedure()
                    #self.MUT.acquire()
                    #self.path = Dijkstra(cst.Home)
                    #self.MUT.release()
                #else:
                    #self.mgt.Stop()
                    
thread_Navigation = Navigation()