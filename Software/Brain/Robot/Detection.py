from threading import Thread, Lock

class Balise_Alert:
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
        self.alert = False
        self.balise = self.NO_ALERT
        self.MUT = Lock()

    def New_Balise(self, balise):
        self.MUT.acquire()
        self.alert = True
        self.Loc = balise
        self.MUT.release()
    
    def Reset(self):
        self.MUT.acquire()
        self.is_alert = False
        self.Loc = self.NO_ALERT
        self.MUT.release()

alert = Balise_Alert()