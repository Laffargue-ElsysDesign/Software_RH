from threading import Thread

from Robot.IHM.interface import mode, cst
from Robot.ManualControl import Keyboard_Read
from Robot.AutoControl import Auto_Control



class Gestionnnaire_Mission(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mission = cst.HOME
        self.manual_control = Keyboard_Read()
        self.auto_control = Auto_Control()

    def init_sequence():
        pass #TBD

    def init_robot(self):
        self.manual_control.Mgt.Stop = False
        self.auto_control.Mgt.Stop = True

    def set_MANUAL():
        pass #TBD

    def set_AUTO():
        pass #TBD

    def run(self):
        ##Set on Auto mode
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == cst.AUTO:
            mode.current_mode == cst.AUTO
        mode.current_mode.MUT.release()
        mode.current_mode == cst.MANUAL
        ##IMU Calibration and first computations check (localisation, ...)
        print("Keyboard")
        #Threads  useful

        self.init_robot()

        self.manual_control.start()
        self.auto_control.start()

        ##Small movement to indicate robot can be used properly
        #self.init_sequence()
        
        #Start of main Thread
        while(True):
            print("Mission")
            ##When Manual
            mode.mode_wanted.MUT.acquire()
            if mode.mode_wanted.mode == cst.MANUAL:
                print("Manual asked")
                mode.mode_wanted.MUT.release()
                 
                 ##If Auto_Thread is on, wait for it to finish.
                if not self.auto_control.Mgt.Waiting:
                    self.auto_control.Mgt.Stop = True
                    while not self.auto_control.Mgt.Waiting:
                        pass
                
                ##If Manual thread is not on, start it 
                if self.manual_control.Mgt.Waiting:
                    self.manual_control.Mgt.Stop = False

                ##Set current values to Manual
                self.set_MANUAL() 

            ##When Auto
            elif mode.mode_wanted.mode == cst.AUTO:
                mode.mode_wanted.MUT.release()
                print("Auto Asked")
                ##If Manual Thread is on, wait for it to  finish
                if not self.manual_control.Mgt.Waiting:
                    self.manual_control.Mgt.Stop = True
                    while not self.auto_control.Mgt.Waiting:
                        pass
                
                ##If Auto Thread is not on, start it
                if self.auto_control.Mgt.Waiting:
                    self.auto_control.Mgt.Stop = False

                ##Set current values to Auto
                self.set_AUTO()
                

