# ManualControl.py

#  Created on: June 2 2022
#      Author: Lenny Laffargue
#

####### Python pakages imports #######
from curses import raw
from threading import Thread
from time import sleep

######### Data imports ############
from Robot.Alerts import alerts, Mgt
from Robot.Evitement import raw_command
from Robot.IHM.interface import mode
import Robot.Permanent.Constants as cst


#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. ManualControl Exiting gracefully')
    exit(0)

class Keyboard_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        self.mgt = Mgt()
        self.interrupt = False

    def Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()

    def Set_Speed(self, x, y, z):
        self.speed_x = x
        self.speed_y = y
        self.speed_z = z

    def Get_Trajectory(self, read_input):
        if read_input==' ':
            #print("Stop")
            self.Set_Speed(0, 0, 0)

        elif read_input=='z':
            #print("Avance")
            self.Set_Speed(0.2, 0, 0)

        elif read_input=='d':
            #print("Droite")
            self.Set_Speed(0, 0.2, 0)

        elif read_input=='q':
            #print("Gauche")
            self.Set_Speed(0, -0.2, 0)

        elif read_input=='s':
            #print("Arriere")
            self.Set_Speed(-0.2, 0, 0)

        elif read_input=='e':
            #print("Nord-est")
            self.Set_Speed(0.2, 0.2, 0)

        elif read_input=='a':
            #print("Nord-ouest")
            self.Set_Speed(0.2, -0.2, 0)

        elif read_input=='w':
            #print("Sud-ouest")
            self.Set_Speed(-0.2, -0.2, 0)

        elif read_input=='x':
            #print("sud-est")
            self.Set_Speed(-0.2, 0.2, 0)

        elif read_input=='"':
            #print("pivot droite")
            self.Set_Speed(0, 0, 0.1)

        elif read_input=='é':
            #print("pivot gauche")
            self.Set_Speed(0, 0, -0.1)

        elif read_input == 'm':
            mode.mode_wanted.mode = cst.modes.AUTO
            self.mgt.Stop()
            
        else:
            print("Input error, please retry")
        return 1    

    def Wait_Start(self):
        print("End of Manual Control")
        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
            
            if (mode.mode_wanted.mode == cst.modes.AUTO) :
                read_input = input()
                if (read_input == 'm'):
                    mode.mode_wanted.MUT.acquire()
                    mode.mode_wanted.mode = cst.modes.MANUAL
                    mode.mode_wanted.MUT.release()
                elif read_input == 'i':
                    print("Balise alert wanted, please input where:")
                    read_input = input()
                    dot = int(read_input)
                    if (dot>=0) and (dot <=16):
                        alerts.Set_Balise_Alert(dot)
                    else:
                        print("not a correct input, ignoring")
                elif read_input == 'b':
                    alerts.Set_Battery_Alert()
                elif read_input == 'r':
                    alerts.Set_Ronde_Alert()
                elif read_input == '1':
                    alerts.Set_NFC_Alert(1, 1)
                elif read_input == '2':
                    alerts.Set_NFC_Alert(2, 2)
                elif read_input == '3':
                    alerts.Set_NFC_Alert(3, 3)
                elif read_input == '4':
                    alerts.Set_NFC_Alert(4, 4)
                elif read_input == '5':
                    alerts.Set_NFC_Alert(5, 5)
                elif read_input == '6':
                    alerts.Set_NFC_Alert(6, 6)
        self.mgt.Is_Not_Waiting()
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        return

    def run(self):
        while not self.interrupt:
            self.Wait_Start()
            print("Start of Manual Control")

            while not self.mgt.Check_Stop() and not self.interrupt:
                #print("Commandes: |Z Nord|D Est|Q Ouest|S Sud|E Nord-Est|A Nord-Ouest|W Sud-Ouest|X Sud-Est|SPACE Stop|\" Pivot Droite|é Pivot Gauche|")
                read_input=input()
                self.Get_Trajectory(read_input)
                raw_command.Set(self.speed_x, self.speed_y, self.speed_z)
            
            raw_command.Set(0, 0, 0)

class IHM_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        self.Alerts = alerts
        self.mgt = Mgt()

    def Set_Speed(self, x, y, z):
        self.speed_x=x
        self.speed_y=y
        self.speed_z=z

    def Get_Trajectory(self):
        if mode.command == cst.orders.NORTH:
            self.Set_Speed(0.2, 0, 0)

        elif mode.command == cst.orders.SOUTH:
            self.Set_Speed(-0.2, 0, 0)

        elif mode.command == cst.orders.EAST:
            self.Set_Speed(0, 0.2, 0)

        elif mode.command == cst.orders.WEST:
            self.Set_Speed(0, -0.2, 0)

        elif mode.command == cst.orders.NORTH_EAST:
            self.Set_Speed(0.2, 0.2, 0)

        elif mode.command == cst.orders.NORTH_WEST:
            self.Set_Speed(0.2, -0.2, 0)

        elif mode.command == cst.orders.SOUTH_EAST:
            self.Set_Speed(-0.2, 0.2, 0)

        elif mode.command == cst.orders.SOUTH_WEST:
            self.Set_Speed(-0.2, -0.2, 0)

        elif mode.command == cst.orders.ROTATE_RIGHT:
            self.Set_Speed(0, 0, 0.1)

        elif mode.command == cst.orders.ROTATE_LEFT:
            self.Set_Speed(0, 0, -0.1)

        elif mode.command == cst.orders.STOP:
            self.Set_Speed(0, 0, 0)

        else:
            self.Set_Speed(0, 0, 0)
            print("Input error. Robot will stop. please retry")
        
    def Wait_Start(self):
        while self.mgt.Check_Stop():
            self.mgt.Is_Waiting()
        self.mgt.Is_Not_Waiting()
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        return

    def run(self):
        while(not self.interrupt):
            sleep(0.5)
            self.Wait_Start()
            mode.command.MUT.acquire()
            read_input=mode.command
            mode.command.MUT.release()
            self.Get_Trajectory(read_input)
            raw_command.Set(self.speed_x, self.speed_y, self.speed_z)
            
        raw_command.Set(0, 0, 0)

thread_manual_control = Keyboard_Read()
#thread_manual_control = IHM_Read()