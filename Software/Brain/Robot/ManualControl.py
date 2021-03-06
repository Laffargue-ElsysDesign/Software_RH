#import Motion.holo32.holo_uart_management as HUM 
from threading import Thread
from Robot.Alerts import alerts, mgt
#import Robot.Motion.holo32.holo_uart_management as HUM
from Robot.IHM.interface import mode
import Robot.Constants as cst

#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. ManualControl Exiting gracefully')
    exit(0)

class Keyboard_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0.5
        self.speed_y=0
        self.speed_z=0
        self.Mgt = mgt()
        self.Interrupt = False

    def set_speed(self, x, y, z):
        self.speed_x = x
        self.speed_y = y
        self.speed_z = z

    def Get_Trajectory(self, read_input):
        if read_input==' ':
            print("Stop")
            self.set_speed(0, 0, 0)

        elif read_input=='z':
            print("Avance")
            self.set_speed(0.5, 0, 0)

        elif read_input=='d':
            print("Droite")
            self.set_speed(0, 0.5, 0)

        elif read_input=='q':
            print("Gauche")
            self.set_speed(0, -0.5, 0)

        elif read_input=='s':
            print("Arriere")
            self.set_speed(-0.5, 0, 0)

        elif read_input=='e':
            print("Nord-est")
            self.set_speed(0.3, 0.3, 0)

        elif read_input=='a':
            print("Nord-ouest")
            self.set_speed(0.3, -0.3, 0)

        elif read_input=='w':
            print("Sud-ouest")
            self.set_speed(-0.3, 0.3, 0)

        elif read_input=='x':
            print("sud-est")
            self.set_speed(-0.3, -0.3, 0)

        elif read_input=='"':
            print("pivot droite")
            self.set_speed(0, 0, 0.3)

        elif read_input=='é':
            print("pivot gauche")
            self.set_speed(0, 0, -0.3)

        elif read_input == 'm':
            mode.mode_wanted.mode = cst.AUTO
            self.Mgt.Stop = True
            
        else:
            print("Input error, please retry")
        return      

    def Wait_Start(self):
        print("End of Manual Control")
        while self.Mgt.Stop and not self.Interrupt:
            self.Mgt.Waiting = True
            
            if (mode.mode_wanted.mode == cst.AUTO) :
                read_input = input()
                if (read_input == 'm'):
                    mode.mode_wanted.MUT.acquire()
                    mode.mode_wanted.mode = cst.MANUAL
                    mode.mode_wanted.MUT.release()
                elif read_input == 'i':
                    alerts.Balise.New = True
                elif read_input == 'b':
                    alerts.Battery = True
                elif read_input == 'r':
                    alerts.Ronde.New = True
        self.Mgt.Waiting = False
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        return

    def run(self):
        while not self.Interrupt:
            self.Wait_Start()
            print("Start of Manual Control")

            while not self.Mgt.Stop and not self.Interrupt:
                print("Commandes: |Z Nord|D Est|Q Ouest|S Sud|E Nord-Est|A Nord-Ouest|W Sud-Ouest|X Sud-Est|SPACE Stop|\" Pivot Droite|é Pivot Gauche|")
                read_input=input()
                self.Get_Trajectory(read_input)
                #HUM.cmd_robot.speed_x=self.speed_x
                #HUM.cmd_robot.speed_y=self.speed_y
                #HUM.cmd_robot.speed_z=self.speed_z
            
            #HUM.cmd_robot.speed_x=0
            #HUM.cmd_robot.speed_y=0
            #HUM.cmd_robot.speed_z=0

class IHM_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        self.Alerts = alerts
        self.Mgt = mgt()

    def set_speed(self, x, y, z):
        self.speed_x=x
        self.speed_y=y
        self.speed_z=z

    def Get_Trajectory(self, read_input):
        if mode.command == cst.NORTH:
            self.set_speed(0.3, 0, 0)

        elif mode.command == cst.SOUTH:
            self.set_speed(-0.3, 0, 0)

        elif mode.command == cst.EAST:
            self.set_speed(0, 0.3, 0)

        elif mode.command == cst.WEST:
            self.set_speed(0, -0.3, 0)

        elif mode.command == cst.NORTH_EAST:
            self.set_speed(0.3, 0.3, 0)

        elif mode.command == cst.NORTH_WEST:
            self.set_speed(0.3, -0.3, 0)

        elif mode.command == cst.SOUTH_EAST:
            self.set_speed(-0.3, 0.3, 0)

        elif mode.command == cst.SOUTH_WEST:
            self.set_speed(-0.3, -0.3, 0)

        elif mode.command == cst.ROTATE_RIGHT:
            self.set_speed(0, 0, 0.3)

        elif mode.command == cst.ROTATE_LEFT:
            self.set_speed(0, 0, -0.3)

        elif mode.command == cst.STOP:
            self.set_speed(0, 0, 0)

        else:
            self.speed_x=0
            self.speed_y=0
            self.speed_z=0
            print("Input error. Robot will stop. please retry")
        
    def Wait_Start(self):
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
        self.Mgt.Waiting = False
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        return

    def run(self):
        while(True):
            self.Wait_Start()
            mode.command.MUT.acquire()
            read_input=mode.command
            mode.command.MUT.release()
            self.Get_Trajectory(read_input)
            #HUM.cmd_robot.speed_x=self.speed_x
            #HUM.cmd_robot.speed_y=self.speed_y
            #HUM.cmd_robot.speed_z=self.speed_z

thread_manual_control = Keyboard_Read()
#thread_manual_control = IHM_Read()