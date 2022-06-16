from threading import Lock

class New_Alert:
    DEFAULT = 0
    STAGIAIRE = 1
    MANAGER = 2
    PAUSE = 3
    REUNION = 4
    ENTREE = 5
    BUREAU = 6
    OPEN_SPACE_ENTREE = 7
    OPEN_SPACE_FOND = 8
    def __init__(self):
        self.is_alert = False
        self.Loc = self.DEFAULT
        self.MUT = Lock()
    
    def Alert(self, goal):
        self.MUT.acquire()
        self.is_alert = True
        self.Loc = goal
        self.MUT.release()
    
    def Reset(self):
        self.MUT.acquire()
        self.is_alert = False
        self.Loc = self.DEFAULT
        self.MUT.release()
    
alert_management = New_Alert()