from threading import Thread, Lock
from time import sleep, time

from numpy import mgrid
from Robot.Alerts import Mgt
import Robot.Localisation as Loc
from Robot.Alerts import alerts
import Robot.Motion.holo32.holo_uart_management as HUM

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Navigation Exiting gracefully')
    exit(0)

def Dijkstra(End):
    pass #TBD

def Compute_Angle(point, old_point):
    return 1, 3 #TBD

def Rotate(Turn):
    if Turn:
        HUM.cmd_robot.speed_x = 0
        HUM.cmd_robot.speed_y = 0
        HUM.cmd_robot.speed_z = 0.3
    else:
        HUM.cmd_robot.speed_x = 0
        HUM.cmd_robot.speed_y = 0
        HUM.cmd_robot.speed_z = -0.3     

def Correct():
    pass #TBD

def Froward():
    HUM.cmd_robot.speed_x = 0.3
    HUM.cmd_robot.speed_y = 0
    HUM.cmd_robot.speed_z = 0

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
    
    def Check_NFC(self, point, old_point):
        output = False
        if alerts.Get_NFC_Alert():
            tag = alerts.Get_NFC_Tag()
            if tag == point:
                #print("point reached")
                output = True
            elif tag == old_point:
                #print("still old point")
                output = False
            else:
                #print("interrupting", point, old_point, tag)
                self.mgt.Stop()
                output = True
            alerts.Reset_Tag_Alert()
        return output

    def Get_to_Point(self, point, old_point):
        if point == old_point:
            return 
            #End = Check_NFC(self.path, point, old_point)
        else:
            Turn, time = Compute_Angle(point, old_point)
            Rotate(Turn)
            sleep(time)
            if self.mgt.Check_Stop():
                return
            while not self.Check_NFC(point, old_point):
                Froward()
            if self.mgt.Check_Stop():
                return
            #Correct()    

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
            T = time()
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