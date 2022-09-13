import cmd
from threading import Thread, Lock
from time import sleep, time
from tkinter import E
from Robot.Alerts import alerts, Mgt, ultrasons
from Robot.holo32.holo_uart_management import cmd_robot

COUNTER = 15

class Raw_Command():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.mgt = Mgt()
        self.MUT = Lock()
    
    def Get(self):
        self.MUT.acquire()
        x = self.x
        y = self.y
        z = self.z
        self.MUT.release()
        return(x, y, z)
    
    def Set(self, x, y, z):
        self.MUT.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.MUT.release()

raw_command = Raw_Command()

class Evitement(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0

        self.W = 0
        self.N = 0
        self.E = 0

        self.DIST_E = 0
        self.DIST_N = 0
        self.DIST_W = 0

        self.C_W = 0
        self.C_N = 0
        self.C_E = 0

        self.mgt = Mgt()
        self.interrupt = False

    def Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()

    def Wait_Start(self):

        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
            self.Get_Raw_Speed()
            self.Set_Command()
            sleep(0.1)
            #print("Evitement Waiting..")
        self.mgt.Is_Not_Waiting()
        return 1

    def Stop(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
    
    def Get_Raw_Speed(self):
        (self.speed_x, self.speed_y, self.speed_z) = raw_command.Get()

    def Set_Command(self):
        cmd_robot.Set_Speed(self.speed_x, self.speed_y, self.speed_z)

    def Zones(self):
        (ALERT_W, Zone_W, DIST_W) = ultrasons.Get_W()
        (ALERT_NW, Zone_NW, DIST_NW) = ultrasons.Get_NW()
        (ALERT_N, Zone_N, DIST_N) = ultrasons.Get_N()
        (ALERT_NE, Zone_NE, DIST_NE) = ultrasons.Get_NE()
        (ALERT_E, Zone_E, DIST_E) = ultrasons.Get_E()
        #print(Zone_W, Zone_NW, Zone_N, Zone_NE, Zone_E)
        
        if Zone_W == 1 or Zone_NW ==1:
            W = 1
        elif Zone_W == 2 or Zone_NW == 2:
            W = 2
        else: 
            W = 0
        
        if Zone_N == 1 or Zone_NW ==1 or Zone_NE ==1:
            N = 1
        elif Zone_N == 2 or Zone_NE == 2 or Zone_NW ==2:
            N = 2
        else:
            N = 0
            
        if Zone_E == 1 or Zone_NE ==1:
            E = 1
        elif Zone_E == 2 or Zone_NE == 2:
            E = 2
        else:
            E = 0

        DIST_W = min(DIST_W, DIST_NW)
        DIST_N = min(DIST_NW, DIST_N, DIST_NE)
        DIST_E = min(DIST_E, DIST_NE)
        
        #print(W, N, E, DIST_W, DIST_N, DIST_E)
        return (W, N, E, DIST_W, DIST_N, DIST_E)


    def Get_US(self):
        (W, N, E, DIST_W, DIST_N, DIST_E) = self.Zones()

        if not (W < 3):
            if not self.C_W == 0:
                self.C_W = self.C_W - 1
            else:
                self.W = 0
                self.DIST_W = DIST_W
        else:
            self.C_W = COUNTER 
            self.W = W
            self.DIST_W = DIST_W

        if not (N < 3):
            if not self.C_N == 0:
                self.C_N = self.C_N - 1
            else:
                self.N = 0
                self.DIST_N = DIST_N
        else:
            self.C_N = COUNTER 
            self.N = N
            self.DIST_N = DIST_N

        if not (E < 3):
            if not self.C_E == 0:
                self.C_E = self.C_E - 1
            else:
                self.E = 0
                self.DIST_E = DIST_E
        else:
            self.C_E = COUNTER 
            self.E = E
            self.DIST_E = DIST_E
        #print(self.E, self.N, self.W)
    def run(self):    
        while not self.interrupt:
            self.Wait_Start()

            while not self.mgt.Check_Stop() and not self.interrupt:

                self.Get_Raw_Speed()

                self.Get_US()

                if (self.W == 1 and self.speed_y < 0) or (self.N == 1 and self.speed_x > 0) or (self.E == 1 and self.speed_y > 0):
                        self.Stop()
                
                if self.W == 2 and self.speed_y < 0:
                        self.speed_y = (self.DIST_W - 10) * self.speed_y / 15

                if self.N == 2 and self.speed_x > 0:
                        self.speed_x = (self.DIST_N - 10) * self.speed_x / 15

                if self.E == 2 and self.speed_y > 0:
                        self.speed_y = (self.DIST_E - 10) * self.speed_y / 15
                    

                self.Set_Command()

                sleep(0.1)
            self.Stop()
            self.Set_Command()

thread_evitement = Evitement()