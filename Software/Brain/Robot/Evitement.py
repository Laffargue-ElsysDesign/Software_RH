import cmd
from threading import Thread, Lock
from time import sleep
from tkinter import E
from Robot.Alerts import alerts, Mgt, ultrasons
from Robot.holo32.holo_uart_management import cmd_robot

COUNTER = 10

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

        self.W = False
        self.NW = False
        self.N = False
        self.NE = False
        self.E = False

        self.C_W = 0
        self.C_NW = 0
        self.C_N = 0
        self.C_NE = 0
        self.C_E = 0

        self.mgt = Mgt()
        self.interrupt = False

    def Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()

    def Wait_Start(self):

        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
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
    
    def Get_US(self):

        if not ultrasons.Get_W()[0]:
            if not self.C_W == 0:
                self.C_W = self.C_W - 1
            else:
                self.W = False
        else:
            self.C_W = COUNTER 
            self.W = True

        if not ultrasons.Get_NW()[0]:
            if not self.C_NW == 0:
                self.C_NW = self.C_NW - 1
            else:
                self.NW = False
        else:
            self.C_NW = COUNTER 
            self.NW = True

        if not ultrasons.Get_N()[0]:
            if not self.C_N == 0:
                self.C_N = self.C_N - 1
            else:
                self.N = False
        else:
            self.C_N = COUNTER 
            self.N = True

        if not ultrasons.Get_NE()[0]:
            if not self.C_NE == 0:
                self.C_NE = self.C_NE - 1
            else:
                self.NE = False
        else:
            self.C_NE = COUNTER 
            self.NE = True
        
        #(E, V, Z)= ultrasons.Get_E()
        #print(E, V, Z)
        if not ultrasons.Get_E()[0]:
            #print("E detected")
            if not self.C_E == 0:
                self.C_E = self.C_E - 1
            else:
                self.E = False
        else:
            self.C_E = COUNTER 
            self.E = True
   
   
    def run(self):
        self.mgt.Restart()
        while not self.interrupt:
            self.Wait_Start()
            print("Start of Evitement")

            while not self.mgt.Check_Stop() and not self.interrupt:
                
                self.Get_Raw_Speed()
                #print("Raw:", self.W, self.NW, self.N, self.NE, self.E)
                self.Get_US()

                if self.N or self.NW:
                    if self.speed_y < 0:
                        self.Stop()

                if self.NW or self.N or self.NE:
                    if self.speed_x > 0:
                        self.Stop()

                if self.E or self.NE:
                    if self.speed_y > 0:
                        self.Stop()
                    
                #print(self.speed_x, self.speed_y, self.speed_z)
                self.Set_Command()
            
            self.Stop()
            self.Set_Command()

thread_evitement = Evitement()