from threading import Thread
from signal import signal, SIGINT

from numpy import where

from IHM.interface import mode
import Motion.holo32.holo_uart_management as HUM
from ManualControl import Keyboard_Read
from AutoControl import Auto_Control

class Gestionnnaire_Mission(Thread):
    IDLE = 0
    INCHARGE = 1
    ALERT = 2
    RETURN = 3
    RONDE = 4
    MANUAL = 5
    def __init__(self):
        Thread.__init__(self)
        self.mission = self.IDLE
    
    def init_sequence():
        pass #TBD

    def init_robot():
        pass #TBD

    def run(self):
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == mode.current_mode.AUTO:
            mode.current_mode == mode.current_mode.MANUAL
        mode.current_mode.MUT.release()
        
        self.init_robot()

        manual_control = Keyboard_Read()
        auto_control = Auto_Control()

        self.init_sequence()

        while(True):
            mode.mode_wanted.MUT.acquire()
            if mode.mode_wanted.mode == mode.MANUAL:
                mode.mode_wanted.MUT.release()
 
                if auto_control.is_alive():
                    thread_auto_stop = True
                    auto_control.join()
                
                if not manual_control.is_alive():
                    manual_control.start()

                self.set_MANUAL() # used to set current mode and current mission to Manual

            elif mode.mode_wanted.mode == mode.AUTO:
                mode.mode_wanted.MUT.release()
                if manual_control.is_alive():
                    thread_manual_stop = True
                    manual_control.join()
                
                if not auto_control.is_alive():
                    auto_control.start()

                self.set_AUTO()
                

