from threading import Thread
from signal import signal, SIGINT

from numpy import where

from IHM.interface import mode, cst
import IHM.interface
import Motion.holo32.holo_uart_management as HUM
from ManualControl import Keyboard_Read
from AutoControl import Auto_Control

class Gestionnnaire_Mission(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mission = self.IDLE
    
    def init_sequence():
        pass #TBD

    def init_robot():
        pass #TBD

    def set_MANUAL():
        pass #TBD

    def set_AUTO():
        pass #TBD

    def run(self):
        ##Set on Auto mode
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == cst.AUTO:
            mode.current_mode == cst.MANUAL
        mode.current_mode.MUT.release()
        
        ##IMU Calibration and first computations check (localisation, ...)
        self.init_robot()

        #Threads  useful
        manual_control = Keyboard_Read()
        manual_control.start()
        auto_control = Auto_Control()
        auto_control.start()

        ##Small movement to indicate robot can be used properly
        self.init_sequence()
        
        #Start of main Thread
        while(True):
            ##When Manual
            mode.mode_wanted.MUT.acquire()
            if mode.mode_wanted.mode == cst.MANUAL:
                mode.mode_wanted.MUT.release()
                 
                 ##If Auto_Thread is on, wait for it to finish.
                if not auto_control.Mgt.Waiting:
                    auto_control.Mgt.Stop = True
                    while not auto_control.Mgt.Waiting:
                        pass
                
                ##If Manual thread is not on, start it 
                if manual_control.Mgt.Waiting:
                    manual_control.Mgt.Stop = False

                ##Set current values to Manual
                self.set_MANUAL() 

            ##When Auto
            elif mode.mode_wanted.mode == cst.AUTO:
                mode.mode_wanted.MUT.release()

                ##If Manual Thread is on, wait for it to  finish
                if not manual_control.Mgt.Waiting:
                    manual_control.Mgt.Stop = True
                    while not auto_control.Mgt.Waiting:
                        pass
                
                ##If Auto Thread is not on, start it
                if auto_control.Mgt.Waiting:
                    auto_control.Mgt.Stop = False

                ##Set current values to Auto
                self.set_AUTO()
                

