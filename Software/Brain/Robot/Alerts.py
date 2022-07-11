from threading import Lock
from Robot.Constants import NOWHERE

class Balise ():
    def __init__(self):
        self.New = False
        self.Dot = 0 #TBD
        self.MUT = Lock()

    def Get_New(self):
        self.MUT.acquire()
        alert = self.New
        self.MUT.release()
        return alert
    
    def Get_Dot(self):
        self.MUT.acquire()
        Dot = self.Dot
        self.MUT.release()
        return Dot
    
    def Set_Balise(self, Dot):
        self.MUT.acquire()
        self.New = True
        self.Dot = Dot
        self.MUT.release()
        return 1

    def Reset(self):
        self.MUT.acquire()
        self.New = False
        self.Dot = NOWHERE
        self.MUT.release()
        return 1

class Battery ():
    def __init__(self):
        self.New = False
        self.MUT = Lock()

    def Get_New(self):
        self.MUT.acquire()
        alert = self.New
        self.MUT.release()
        return alert
    
    def Set_New(self):
        self.MUT.acquire()
        self.New = True
        self.MUT.release()
        return 1
    
    def Reset(self):
        self.MUT.acquire()
        self.New = False
        self.MUT.release()
        return 1

class Ronde ():
    def __init__(self):
        self.New = False
        self.MUT = Lock()
    
    def Get_New(self):
        self.MUT.acquire()
        alert = self.New
        self.MUT.release()
        return alert
    
    def Set_New(self):
        self.MUT.acquire()
        self.New = True
        self.MUT.release()
        return 1
    
    def Reset(self):
        self.MUT.acquire()
        self.New = False
        self.MUT.release()
        return 1

class Alerts ():
    def __init__(self):
        self.Battery = Battery()
        self.Ronde = Ronde()
        self.Balise = Balise()
    
    def Get_Battery_Alert(self):
        return self.Battery.Get_New()

    def Set_Battery_Alert(self):
        return self.Battery.Set_New()

    def Reset_Battery_Alert(self):
        return self.Battery.Reset()

    def Get_Balise_Alert(self):
        return self.Balise.Get_New()
    
    def Get_Balise_Dot(self):
        return self.Balise.Get_Dot()

    def Set_Balise_Alert(self, Dot):
        return self.Balise.Set_Balise(Dot)
    
    def Reset_Balise_Alert(self):
        return self.Balise.Reset()
    
    def Get_Ronde_Alert(self):
        return self.Ronde.Get_New()
    
    def Set_Ronde_Alert(self):
        return self.Ronde.Set_New()
    
    def Reset_Ronde_Alert(self):
        return self.Ronde.Reset() 

alerts = Alerts()

class mgt():
    def __init__(self):
        self.Stop = True
        self.Waiting = True