#import Motion.holo32.holo_uart_management as HUM 
from threading import Thread
from Robot.IHM.interface import mode, cst
from Robot.Navigation import mgt
from Robot.Alerts import Alerts

#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)



class Keyboard_Read(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.speed_x=0.5
        self.speed_y=0
        self.speed_z=0
        self.Mgt = mgt()
    def Get_Trajectory(self, read_input):
        if read_input==' ':
            print("Stop")
            self.speed_x=0
            self.speed_y=0
            self.speed_z=0
        elif read_input=='z':
            print("Avance")
            self.speed_x=0.5
            self.speed_y=0
            self.speed_z=0
        elif read_input=='d':
            print("Droite")
            self.speed_x=0
            self.speed_y=0.5
            self.speed_z=0
        elif read_input=='q':
            print("Gauche")
            self.speed_x=0
            self.speed_y=-0.5
            self.speed_z=0
        elif read_input=='s':
            print("Arriere")
            self.speed_x=-0.5
            self.speed_y=0
            self.speed_z=0
        elif read_input=='e':
            print("Nord-est")
            self.speed_x=0.3
            self.speed_y=0.3
            self.speed_z=0
        elif read_input=='a':
            print("Nord-ouest")
            self.speed_x=0.3
            self.speed_y=-0.3
            self.speed_z=0
        elif read_input=='w':
            print("Sud-ouest")
            self.speed_x=-0.3
            self.speed_y=0.3
            self.speed_z=0
        elif read_input=='x':
            print("sud-est")
            self.speed_x=-0.3
            self.speed_y=-0.3
            self.speed_z=0
        elif read_input=='"':
            print("pivot droite")
            self.speed_x=-0
            self.speed_y=0
            self.speed_z=0.3
        elif read_input=='é':
            print("pivot gauche")
            self.speed_x=0
            self.speed_y=0
            self.speed_z=-0.3
        elif read_input == 'm':
            mode.mode_wanted.mode = cst.AUTO
            self.Mgt.Stop = True
        else:
            print("Input error, please retry")
        return      

    def Wait_Start(self):
        print("End of Manual Control")
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
            
            if (mode.mode_wanted.mode == cst.AUTO) :
                read_input = input()
                if (read_input == 'm'):
                    mode.mode_wanted.MUT.acquire()
                    mode.mode_wanted.mode = cst.MANUAL
                    mode.mode_wanted.MUT.release()
        self.Mgt.Waiting = False
        self.speed_x=0
        self.speed_y=0
        self.speed_z=0
        return

    def run(self):
        while True:
            self.Wait_Start()
            print("Start of Manual Control")

            while not self.Mgt.Stop:
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
        self.Alerts = Alerts()
        self.Mgt = mgt()
    def Get_Trajectory(self, read_input):
        if mode.command == mode.command.NORTH:
            self.speed_x=0.3
            self.speed_y=0
            self.speed_z=0
        elif mode.command == mode.command.SOUTH:
            self.speed_x=-0.3
            self.speed_y=0
            self.speed_z=0
        elif mode.command == mode.command.EAST:
            self.speed_x=0
            self.speed_y=0.3
            self.speed_z=0
        elif mode.command == mode.command.WEST:
            self.speed_x=0
            self.speed_y=-0.3
            self.speed_z=0
        elif mode.command == mode.command.NORTH_EAST:
            self.speed_x=-0.3
            self.speed_y=0.3
            self.speed_z=0
        elif mode.command == mode.command.NORTH_WEST:
            self.speed_x=0.3
            self.speed_y=-0.3
            self.speed_z=0
        elif mode.command == mode.command.SOUTH_EAST:
            self.speed_x=-0.3
            self.speed_y=0.3
            self.speed_z=0
        elif mode.command == mode.command.SOUTH_WEST:
            self.speed_x=-0.3
            self.speed_y=-0.3
            self.speed_z=0
        elif mode.command == mode.command.ROTATE_RIGHT:
            self.speed_x=0
            self.speed_y=0
            self.speed_z=0.3
        elif mode.command == mode.command.ROTATE_LEFT:
            self.speed_x=-0
            self.speed_y=0
            self.speed_z=-0.3
        elif mode.command == mode.command.STOP:
            self.speed_x=0
            self.speed_y=0
            self.speed_z=0
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
            mode.MUT.release()
            self.Get_Trajectory(read_input)
            #HUM.cmd_robot.speed_x=self.speed_x
            #HUM.cmd_robot.speed_y=self.speed_y
            #HUM.cmd_robot.speed_z=self.speed_z
