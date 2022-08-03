from threading import Thread
from Robot.Alerts import alerts, Mgt
import Robot.holo32.holo_uart_management as HUM
from Robot.IHM.interface import mode
import Robot.Constants as cst
from time import sleep

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
            self.Set_Speed(0.3, 0, 0)

        elif read_input=='d':
            #print("Droite")
            self.Set_Speed(0, 0.3, 0)

        elif read_input=='q':
            #print("Gauche")
            self.Set_Speed(0, -0.3, 0)

        elif read_input=='s':
            #print("Arriere")
            self.Set_Speed(-0.3, 0, 0)

        elif read_input=='e':
            #print("Nord-est")
            self.Set_Speed(0.3, 0.3, 0)

        elif read_input=='a':
            #print("Nord-ouest")
            self.Set_Speed(0.3, -0.3, 0)

        elif read_input=='w':
            #print("Sud-ouest")
            self.Set_Speed(-0.3, -0.3, 0)

        elif read_input=='x':
            #print("sud-est")
            self.Set_Speed(-0.3, 0.3, 0)

        elif read_input=='"':
            #print("pivot droite")
            self.Set_Speed(0, 0, 0.3)

        elif read_input=='é':
            #print("pivot gauche")
            self.Set_Speed(0, 0, -0.3)

        elif read_input == 'm':
            mode.mode_wanted.mode = cst.AUTO
            self.mgt.Stop()
            
        else:
            print("Input error, please retry")
        return 1    

    def Wait_Start(self):
        print("End of Manual Control")
        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
            
            if (mode.mode_wanted.mode == cst.AUTO) :
                read_input = input()
                if (read_input == 'm'):
                    mode.mode_wanted.MUT.acquire()
                    mode.mode_wanted.mode = cst.MANUAL
                    mode.mode_wanted.MUT.release()
                elif read_input == 'i':
                    alerts.Set_Balise_Alert(4)
                elif read_input == 'b':
                    alerts.Set_Battery_Alert()
                elif read_input == 'r':
                    alerts.Set_Ronde_Alert()
                elif read_input == '1':
                    alerts.Set_NFC_Alert(1)
                elif read_input == '2':
                    alerts.Set_NFC_Alert(2)
                elif read_input == '3':
                    alerts.Set_NFC_Alert(3)
                elif read_input == '4':
                    alerts.Set_NFC_Alert(4)
                elif read_input == '5':
                    alerts.Set_NFC_Alert(5)
                elif read_input == '6':
                    alerts.Set_NFC_Alert(6)
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
                #HUM.cmd_robot.speed_x=self.speed_x
                #HUM.cmd_robot.speed_y=self.speed_y
                #HUM.cmd_robot.speed_z=self.speed_z
                HUM.cmd_robot.Set_Speed(self.speed_x, self.speed_y, self.speed_z)
            
            #HUM.cmd_robot.speed_x=0
            #HUM.cmd_robot.speed_y=0
            #HUM.cmd_robot.speed_z=0
            HUM.cmd_robot.Set_Speed(0, 0, 0)

class IHM_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        self.Alerts = alerts
        self.mgt = Mgt()

    def set_speed(self, x, y, z):
        self.speed_x=x
        self.speed_y=y
        self.speed_z=z

    def Get_Trajectory(self, read_input):
        if mode.command == cst.NORTH:
            self.Set_Speed(0.3, 0, 0)

        elif mode.command == cst.SOUTH:
            self.Set_Speed(-0.3, 0, 0)

        elif mode.command == cst.EAST:
            self.Set_Speed(0, 0.3, 0)

        elif mode.command == cst.WEST:
            self.Set_Speed(0, -0.3, 0)

        elif mode.command == cst.NORTH_EAST:
            self.Set_Speed(0.3, 0.3, 0)

        elif mode.command == cst.NORTH_WEST:
            self.Set_Speed(0.3, -0.3, 0)

        elif mode.command == cst.SOUTH_EAST:
            self.Set_Speed(-0.3, 0.3, 0)

        elif mode.command == cst.SOUTH_WEST:
            self.Set_Speed(-0.3, -0.3, 0)

        elif mode.command == cst.ROTATE_RIGHT:
            self.Set_Speed(0, 0, 0.3)

        elif mode.command == cst.ROTATE_LEFT:
            self.Set_Speed(0, 0, -0.3)

        elif mode.command == cst.STOP:
            self.Set_Speed(0, 0, 0)

        else:
            self.speed_x=0
            self.speed_y=0
            self.speed_z=0
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
        while(True):
            sleep(0.5)
            self.Wait_Start()
            mode.command.MUT.acquire()
            read_input=mode.command
            mode.command.MUT.release()
            self.Get_Trajectory(read_input)
            #HUM.cmd_robot.speed_x=self.speed_x
            #HUM.cmd_robot.speed_y=self.speed_y
            #HUM.cmd_robot.speed_z=self.speed_z
            #HUM.cmd_robot.Set_Speed(self.speed_x, self.speed_y, self.speed_z)

thread_manual_control = Keyboard_Read()
#thread_manual_control = IHM_Read()