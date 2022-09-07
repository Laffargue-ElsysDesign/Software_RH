import cmd
from threading import Thread, Lock
from time import sleep
from tkinter import E
from Robot.Alerts import alerts, Mgt, ultrasons
from Robot.holo32.holo_uart_management import cmd_robot

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
    
    def Get_Raw_Speed(self):
        (self.speed_x, self.speed_y, self.speed_z) = raw_command.Get()

    def Set_Command(self):
        cmd_robot.Set_Speed(self.speed_x, self.speed_y, self.speed_z)
   
    def run(self):
        while not self.interrupt:
            self.Wait_Start()
            print("Start of Auto Control")

            while not self.mgt.Check_Stop() and not self.interrupt:
                
                self.Get_Raw_Speed()

                if ultrasons.Get_W()[0] or ultrasons.Get_NW()[0]:
                    if self.speed_y < 0:
                        self.speed_x = 0
                        self.speed_y = 0
                        self.speed_z = 0

                if ultrasons.Get_NW()[0] or ultrasons.Get_N()[0] or ultrasons.Get_NE()[0]:
                    if self.speed_x > 0:
                        self.speed_x = 0
                        self.speed_y = 0
                        self.speed_z = 0

                if ultrasons.Get_E()[0] or ultrasons.Get_NE()[0]:
                    if self.speed_y > 0:
                        self.speed_x = 0
                        self.speed_y = 0
                        self.speed_z = 0
                    

                self.Set_Command()
            
            self.speed_x = 0
            self.speed_y = 0
            self.speed_z = 0
            self.Set_Command()

thread_evitement = Evitement()