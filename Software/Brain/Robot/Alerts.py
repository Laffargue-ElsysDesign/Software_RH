from threading import Lock
class Balise ():
    def __init__(self):
        self.New = False
        self.Loc = 0 #TBD
        self.MUT = Lock()

class Alerts():
    def __init__(self):
        self.Battery = False
        self.Ronde = False
        self.Balise = Balise()