from threading import Lock


class Class_Command:
    STOP=0
    NORTH=1
    SOUTH=2
    EAST=3
    WEST=4
    NORTH_WEST=5
    NORTH_EAST=6
    SOUTH_WEST=7
    SOUTH_EAST=8
    ROTATE_RIGHT=9
    ROTATE_LEFT=10
    def __init__(self):
        self.order = self.STOP
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.MUT = Lock()

    def Convert_Button_to_order(self, button):
        if button.get("buttonN"):
            self.MUT.acquire()
            self.order = self.NORTH
            self.x = 0.2
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonS"):
            self.MUT.acquire()
            self.order = self.SOUTH
            self.x = -0.2
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonSE"):
            self.MUT.acquire()
            self.order = self.SOUTH_EAST
            self.x = -0.2
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonSW"):
            self.MUT.acquire()
            self.order = self.SOUTH_WEST
            self.x = -0.2
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonNE"):
            self.MUT.acquire()
            self.order = self.NORTH_EAST
            self.x = 0.2
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonNW"):
            self.MUT.acquire()
            self.order = self.NORTH_WEST
            self.x = 0.2
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonStop"):
            self.MUT.acquire()
            self.order = self.STOP
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonE"):
            self.MUT.acquire()
            self.order = self.EAST
            self.x = 0.0
            self.y = 0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonW"):
            self.MUT.acquire()
            self.order = self.WEST
            self.x = 0.0
            self.y = -0.2
            self.z = 0.0
            self.MUT.release()
        elif button.get("buttonRR"):
            self.MUT.acquire()
            self.order = self.ROTATE_RIGHT
            self.x = 0.0
            self.y = 0.0
            self.z = 0.5
            self.MUT.release()
        elif button.get("buttonRL"):
            self.MUT.acquire()
            self.order = self.ROTATE_LEFT
            self.x = 0.0
            self.y = 0.0
            self.z = -0.5
            self.MUT.release()
        print(self.order)

class Current_Mission:
    IDLE = 0
    INCHARGE = 1
    ALERT = 2
    RETURN = 3
    RONDE = 4
    MANUAL = 5
    def __init__(self):
        self.mission = self.IDLE
        self.MUT = Lock()

    def Set_Idle(self):
        self.MUT.acquire()
        self.mission = self.IDLE
        self.MUT.release()
    
    def Set_InCharge(self):
        self.MUT.acquire()
        self.mission = self.INCHARGE
        self.MUT.release()

    def Set_Alert(self):
        self.MUT.acquire()
        self.mission = self.ALERT
        self.MUT.release()

    def Set_Return(self):
        self.MUT.acquire()
        self.mission = self.RETURN
        self.MUT.release()

    def Set_Ronde(self):
        self.MUT.acquire()
        self.mission = self.RONDE
        self.MUT.release()

    def Set_Manual(self):
        self.MUT.acquire()
        self.mission = self.MANUAL
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
    AUTO=0
    MANUAL=1
    def __init__(self):
        self.mode = self.AUTO
        self.MUT = Lock()

class Mode_Wanted:
    AUTO=0
    MANUAL=1
    def __init__(self):
        self.mode = self.AUTO
        self.MUT = Lock()

    def Set_AUTO(self):
        self.MUT.acquire()
        self.mode = self.AUTO
        self.MUT.release()

    def Set_MANUAL(self):
        self.MUT.acquire()
        self.mode = self.MANUAL
        self.MUT.release()

class Mode:
    NO_ALERT = 0
    STAGIAIRE = 1
    MANAGER = 2
    PAUSE = 3
    REUNION = 4
    ENTREE = 5
    BUREAU = 6
    OPEN_SPACE_ENTREE = 7
    OPEN_SPACE_FOND = 8
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
        self.current_mode.mode = self.mode_wanted.AUTO
        self.current_mode.MUT.release()
        self.command.MUT.acquire()
        self.command.order = self.command.STOP
        self.command.MUT.release()
        self.mission.Set_Idle()
        print(self.mode_wanted.mode, self.command.order)

    def Set_MANUAL(self):
        self.current_mode.MUT.acquire()
        self.current_mode.mode = self.mode_wanted.MANUAL
        self.current_mode.MUT.release()
        self.ronde.Disable_Ronde()
        self.command.MUT.acquire()
        self.command.order = self.command.STOP
        self.command.MUT.release()
        self.mission.Set_Manual()
        
        print(self.mode_wanted.mode, self.command.order)
    
    def Is_Auto(self):
        output = True
        self.current_mode.MUT.acquire()
        if (self.current_mode.mode == self.current_mode.MANUAL):
            output = False
        
        return output

mode = Mode()      