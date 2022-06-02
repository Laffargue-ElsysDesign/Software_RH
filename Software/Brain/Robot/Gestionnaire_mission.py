from threading import Thread
import Robot.Constants as cst
from Robot.IHM.interface import mode
from Robot.ManualControl import thread_manual_control as tmc
from Robot.AutoControl import thread_auto_control as tac
from time import sleep
#import Motion.holo32.holo_uart_management as HUM


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Gestionnaire Exiting gracefully')
    exit(0)


class Gestionnnaire_Mission(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mission = cst.HOME
        self.manual_control = tmc
        self.auto_control = tac
        self.interrupt = False

    def Interrupt(self):
        self.interrupt = True

    def init_sequence():
        pass #TBD

    def init_robot(self):
        pass

    def set_MANUAL(self):

        ##If Auto_Thread is on, wait for it to finish.
        if not self.auto_control.mgt.Check_Waiting():
            self.auto_control.mgt.Stop()
            while not self.auto_control.mgt.Check_Waiting() and not self.interrupt:
                sleep(0.1)
        ##If Manual thread is not on, start it 
        if self.manual_control.mgt.Check_Waiting():
            self.manual_control.mgt.Restart()

    def set_AUTO(self):
        ##If Manual Thread is on, wait for it to  finish
        if not self.manual_control.mgt.Check_Waiting():
            self.manual_control.mgt.Stop()
            while not self.manual_control.mgt.Check_Waiting() and not self.interrupt:
                sleep(0.1)
        
        ##If Auto Thread is not on, start it
        if self.auto_control.mgt.Check_Waiting():
            self.auto_control.mgt.Restart() 

    def run(self):
        ##Set on Auto mode
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == cst.AUTO:
            mode.current_mode == cst.AUTO
        mode.current_mode.MUT.release()
        ##IMU Calibration and first computations check (localisation, ...)

        #Threads  useful

        #self.init_robot()

        ##Small movement to indicate robot can be used properly
        #self.init_sequence()

        #Start of main Thread
        while(not self.interrupt):

            ##When Manual
            mode.mode_wanted.MUT.acquire()
            if mode.mode_wanted.mode == cst.MANUAL:
                mode.mode_wanted.MUT.release()
            ##Set current values to Manual
                self.set_MANUAL() 

            ##When Auto
            elif mode.mode_wanted.mode == cst.AUTO:
                mode.mode_wanted.MUT.release()
               

                ##Set current values to Auto
                self.set_AUTO()

thread_gestionnaire = Gestionnnaire_Mission()