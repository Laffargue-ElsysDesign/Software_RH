from threading import Thread
from signal import signal, SIGINT

from numpy import where

from IHM.interface import mode
from IHM import Create_App
from Motion.Localisation import coordinate
import Motion.holo32.holo_uart_management as HUM
from Energie.Battery import alert_battery
from Detection import balise_alert
from Motion.Gestionnaire_alertes import alert_management
import Motion.holo32.holo_uart_management 

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

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
        ###self.battery = False
    
    def init_sequence():
        a=1

    def init_AUTO_Mode():
        HUM.cmd_robot.MUT.acquire()
        HUM.cmd_robot.speed_x=0.0
        HUM.cmd_robot.speed_y=0.0
        HUM.cmd_robot.speed_z=0.0
        HUM.cmd_robot.MUT.release()

    def init_MANUAL_Mode():
        #Navigation Interrupt + Gestion alerte Interrupt + Battery interrupt
        #Ronde stop
        #Make sure the car is stopped the car
        HUM.cmd_robot.MUT.acquire()
        HUM.cmd_robot.speed_x=0.0
        HUM.cmd_robot.speed_y=0.0
        HUM.cmd_robot.speed_z=0.0
        HUM.cmd_robot.MUT.release()

    def is_wanted_Mode():
        mode.current_mode.MUT.acquire()
        mode.mode_wanted.MUT.acquire()
        output = (mode.mode_wanted.mode == mode.current_mode.mode)
        mode.current_mode.MUT.release()
        mode.mode_wanted.MUT.release()
        return output



    def run(self):
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == mode.current_mode.AUTO:
            mode.current_mode == mode.current_mode.MANUAL
        mode.current_mode.MUT.release()

        coordinate.MUT.acquire()
        if not coordinate.coo == coordinate.home:
            print("error loc")
        coordinate.MUT.release()

        self.init_sequence()

        while(True):
            mode.current_mode.MUT.acquire()
            if mode.current_mode.mode == mode.current_mode.AUTO:
                mode.current_mode.MUT.release()

                
                if self.is_wanted_Mode():

                    self.init_MANUAL_Mode()

                    mode.Set_MANUAL()

                    self.mission = self.MANUAL

                elif balise_alert.is_Alert():
                    alert_management.Alert(balise_alert.where_Alert())
                    balise_alert.Reset()
                    mode.mission.Set_Alert()
                    ###self.battery = True

            elif mode.current_mode.mode == mode.current_mode.MANUAL:
                mode.current_mode.MUT.release()

                if self.is_wanted_Mode():

                    self.init_AUTO_Mode()

                    mode.Set_AUTO()
                
                #elif alert_battery.is_Alert():
                elif balise_alert.is_Alert():
                    mode.alert = True
                    mode.alert = balise_alert.where_Alert()
                    balise_alert.Reset()

                else:
                    HUM.cmd_robot.MUT.acquire()
                    HUM.cmd_robot.speed_x = mode.command.x
                    HUM.cmd_robot.speed_y = mode.command.y
                    HUM.cmd_robot.speed_z = mode.command.z
                    HUM.cmd_robot.MUT.release()

    def run2(self):
        mode.current_mode.MUT.acquire()
        if not mode.current_mode == mode.current_mode.AUTO:
            mode.current_mode == mode.current_mode.MANUAL
        mode.current_mode.MUT.release()

        coordinate.MUT.acquire()
        if not coordinate.coo == coordinate.home:
            print("error loc")
        coordinate.MUT.release()

        self.init_sequence()

        while(True):
            mode.current_mode.MUT.acquire()
            if mode.current_mode.mode == mode.current_mode.AUTO:
                mode.current_mode.MUT.release()

                
                if self.is_wanted_Mode():

                    self.init_MANUAL_Mode()

                    mode.Set_MANUAL()

                    self.mission = self.MANUAL

                elif balise_alert.is_Alert():
                    alert_management.Alert(balise_alert.where_Alert())
                    balise_alert.Reset()
                    mode.mission.Set_Alert()
                    ###self.battery = True

            elif mode.current_mode.mode == mode.current_mode.MANUAL:
                mode.current_mode.MUT.release()

                if self.is_wanted_Mode():

                    self.init_AUTO_Mode()

                    mode.Set_AUTO()
                
                #elif alert_battery.is_Alert():
                elif balise_alert.is_Alert():
                    mode.alert = True
                    mode.alert = balise_alert.where_Alert()
                    balise_alert.Reset()

                else:
                    HUM.cmd_robot.MUT.acquire()
                    HUM.cmd_robot.speed_x = mode.command.x
                    HUM.cmd_robot.speed_y = mode.command.y
                    HUM.cmd_robot.speed_z = mode.command.z
                    HUM.cmd_robot.MUT.release()


    

