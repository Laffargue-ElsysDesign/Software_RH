from threading import Lock

class New_Alert:
    DEFAULT = 0
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
    
new_alert = New_Alert()