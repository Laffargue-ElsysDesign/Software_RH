# interface.py

#  Created on: June 2 2022
#      Author: Lenny Laffargue
#

########## Python packages imports ##########
from threading import Lock

######### Data imports ############
import Robot.Permanent.Constants as cst

class Class_Command:  
    def __init__(self):
        self.order = cst.orders.STOP
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.MUT = Lock()

    def Convert_Button_to_order(self, button):
        if button.get("buttonN"):
            self.MUT.acquire()
            self.order = cst.orders.NORTH
            self.x = 0.2
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonS"):
            self.MUT.acquire()
            self.order = cst.orders.SOUTH
            self.x = -0.2
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonSE"):
            self.MUT.acquire()
            self.order = cst.orders.SOUTH_EAST
            self.x = -0.2
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonSW"):
            self.MUT.acquire()
            self.order = cst.orders.SOUTH_WEST
            self.x = -0.2
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonNE"):
            self.MUT.acquire()
            self.order = cst.orders.NORTH_EAST
            self.x = 0.2
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonNW"):
            self.MUT.acquire()
            self.order = cst.orders.NORTH_WEST
            self.x = 0.2
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonStop"):
            self.MUT.acquire()
            self.order = cst.orders.STOP
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonE"):
            self.MUT.acquire()
            self.order = cst.orders.EAST
            self.x = 0.0
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonW"):
            self.MUT.acquire()
            self.order = cst.orders.WEST
            self.x = 0.0
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonRR"):
            self.MUT.acquire()
            self.order = cst.orders.ROTATE_RIGHT
            self.x = 0.0
            self.y = 0.0
            self.z = 0.5
            self.MUT.release()
        elif button.get("buttonRL"):
            self.MUT.acquire()
            self.order = cst.orders.ROTATE_LEFT
            self.x = 0.0
            self.y = 0.0
            self.z = -0.5
            self.MUT.release()
        print(self.order)

class Current_Mission:
    def __init__(self):
        self.mission = cst.missions.HOME
        self.MUT = Lock()

    def Set_Idle(self):
        self.MUT.acquire()
        self.mission = cst.missions.HOME
        self.MUT.release()
    
    def Set_InCharge(self):
        self.MUT.acquire()
        self.mission = cst.missions.IN_CHARGE
        self.MUT.release()

    def Set_Alert(self):
        self.MUT.acquire()
        self.mission = cst.missions.ALERT
        self.MUT.release()

    def Set_Return(self):
        self.MUT.acquire()
        self.mission = cst.missions.RETURN
        self.MUT.release()

    def Set_Ronde(self):
        self.MUT.acquire()
        self.mission = cst.missions.RONDE
        self.MUT.release()

    def Set_Manual(self):
        self.MUT.acquire()
        self.mission = cst.missions.MANUAL
        self.MUT.release()

class Ronde_Wanted:
    def __init__(self):
        self.ronde = False
        self.MUT = Lock()

    def Enable_Ronde(self):
        self.MUT.acquire()
        self.ronde=True
        self.MUT.release()
        
    def Disable_Ronde(self):
        self.MUT.acquire()
        self.ronde=False
        self.MUT.release()

class Current_Mode:
    def __init__(self):
        self.mode = cst.modes.AUTO
        self.MUT = Lock()

class Mode_Wanted:
    def __init__(self):
        self.mode = cst.modes.AUTO
        self.MUT = Lock()

    def Set_AUTO(self):
        self.MUT.acquire()
        self.mode = cst.modes.AUTO
        self.MUT.release()

    def Set_MANUAL(self):
        self.MUT.acquire()
        self.mode = cst.modes.MANUAL
        self.MUT.release()

class Mode:
    
    def __init__(self):
        self.mode_wanted = Mode_Wanted()
        self.current_mode = Current_Mode()
        self.command = Class_Command()
        self.mission = Current_Mission()
        self.ronde = Ronde_Wanted()
        self.alert = False
        self.Loc = 0

    def Set_AUTO(self):
        self.current_mode.MUT.acquire()
        self.current_mode.mode = cst.modes.AUTO
        self.current_mode.MUT.release()
        self.command.MUT.acquire()
        self.command.order = cst.orders.STOP
        self.command.MUT.release()
        self.mission.Set_Idle()
        print(self.mode_wanted.mode, self.command.order)

    def Set_MANUAL(self):
        self.current_mode.MUT.acquire()
        self.current_mode.mode = cst.modes.MANUAL
        self.current_mode.MUT.release()
        self.ronde.Disable_Ronde()
        self.command.MUT.acquire()
        self.command.order = cst.orders.STOP
        self.command.MUT.release()
        self.mission.Set_Manual()
        
        print(self.mode_wanted.mode, self.command.order)
    
    def Is_Auto(self):
        output = True
        self.current_mode.MUT.acquire()
        if (self.current_mode.mode == cst.modes.MANUAL):
            output = False
        
        return output

mode = Mode()      