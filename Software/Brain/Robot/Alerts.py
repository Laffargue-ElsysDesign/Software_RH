from threading import Lock
class Balise ():
    def __init__(self):
        self.New = False
        self.Loc = 0 #TBD
        self.MUT = Lock()
class Ronde ():
    def __init__(self):
        self.New = False
        self.path = 0 #TBD
class Alerts():
    def __init__(self):
        self.Battery = False
        self.Ronde = Ronde()
        self.Balise = Balise()
alerts = Alerts()
