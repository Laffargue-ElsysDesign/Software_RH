from msilib.schema import Class
from threading import Lock
from Robot.Constants import NOWHERE

##Class Balise used for Alerts management
class State_Balise():
    def __init__(self):
        self.new = False
        self.dot = 0 #TBD
        self.MUT = Lock()

    def Get_New(self):
        self.MUT.acquire()
        alert = self.new
        self.MUT.release()
        return alert
    
    def Get_Dot(self):
        self.MUT.acquire()
        Dot = self.dot
        self.MUT.release()
        return Dot
    
    def Set_Balise(self, Dot):
        self.MUT.acquire()
        self.new = True
        self.dot = Dot
        self.MUT.release()
        return 1

    def Reset(self):
        self.MUT.acquire()
        self.new = False
        self.dot = NOWHERE
        self.MUT.release()
        return 1

##Class Battery used for Alerts management
class State_Battery ():
    def __init__(self):
        self.new = False
        self.MUT = Lock()

    def Get_New(self):
        self.MUT.acquire()
        alert = self.new
        self.MUT.release()
        return alert
    
    def Set_New(self):
        self.MUT.acquire()
        self.new = True
        self.MUT.release()
        return 1
    
    def Reset(self):
        self.MUT.acquire()
        self.new = False
        self.MUT.release()
        return 1

##Class Ronde used for Alerts management
class State_Ronde():
    def __init__(self):
        self.new = False
        self.MUT = Lock()
    
    def Get_New(self):
        self.MUT.acquire()
        alert = self.new
        self.MUT.release()
        return alert
    
    def Set_New(self):
        self.MUT.acquire()
        self.new = True
        self.MUT.release()
        return 1
    
    def Reset(self):
        self.MUT.acquire()
        self.new = False
        self.MUT.release()
        return 1

##Class Alerts combining all Alerts which can create a new objective
class Alerts ():
    def __init__(self):
        self.battery = State_Battery()
        self.ronde = State_Ronde()
        self.balise = State_Balise()
    
    def Get_Battery_Alert(self):
        return self.battery.Get_New()

    def Set_Battery_Alert(self):
        return self.battery.Set_New()

    def Reset_Battery_Alert(self):
        return self.battery.Reset()

    def Get_Balise_Alert(self):
        return self.balise.Get_New()
    
    def Get_Balise_Dot(self):
        return self.balise.Get_Dot()

    def Set_Balise_Alert(self, Dot):
        return self.balise.Set_Balise(Dot)
    
    def Reset_Balise_Alert(self):
        return self.balise.Reset()
    
    def Get_Ronde_Alert(self):
        return self.ronde.Get_New()
    
    def Set_Ronde_Alert(self):
        return self.ronde.Set_New()
    
    def Reset_Ronde_Alert(self):
        return self.ronde.Reset() 

##element alerts used by all threads who needs to share these informations
alerts = Alerts()

##Class mgt is usefull to stop/Restart a Thread
class mgt():
    def __init__(self):
        self.stop = True
        self.waiting = True

    def Stop(self):
        self.stop = True
   
    def Restart(self):
        self.stop = False
    
    def Is_Waiting(self):
        self.waiting = True
        
    def Is_Not_Waiting(self):
        self.waiting = False

    def Check_Stop(self):
        return self.stop
        
    def Check_Waiting(self):
        return self.waiting

##Class Zone storing all infos on a Zone
class Zone():
    def __init__(self):
        self.State = False
        self.Zone = 0
        self.Value = 0
        self.MUT = Lock()
    
    def Set(self, State, Zone, Value):
        self.MUT.acquire()
        self.State = State
        self.Zone = Zone
        self.Value = Value
        self.MUT.release()
        return(1)
    
    def Get(self):
        self.MUT.acquire()
        State = self.State
        Zone = self.Zone
        Value = self.Value
        self.MUT.release()
        return (State, Zone, Value)

##Class Ultrasons For Avoidance featureContainging all infos on every Zones
class Class_Ultrasons():
    def __init__(self):
        self.W = Zone()
        self.NW = Zone()
        self.N = Zone()
        self.NE = Zone()
        self.E = Zone()
    
    def Get_W(self):
        return self.W.Get()

    def Set_W(self, State, Zone, Value):
        return self.W.Set(State, Zone, Value)

    def Reset_W(self):
        return self.Set_W(False, 0, 0)
    
    def Get_NW(self):
        return self.NW.Get()
    
    def Set_NW(self, State, Zone, Value):
        return self.NW.Set(State, Zone, Value)
    
    def Reset_NW(self):
        return self.Set_NW(False, 0, 0)

    def Get_N(self):
        return self.N.Get()
    
    def Set_N(self, State, Zone, Value):
        return self.N.Set(State, Zone, Value)
    
    def Reset_N(self):
        return self.Set_N(False, 0, 0)

    def Get_NE(self):
        return self.NE.Get()
    
    def Set_NE(self, State, Zone, Value):
        return self.NE.Set(State, Zone, Value)
    
    def Reset_NE(self):
        return self.Set_NE(False, 0, 0)

    def Get_E(self):
        return self.E.Get()
    
    def Set_E(self, State, Zone, Value):
        return self.E.Set(State, Zone, Value)
    
    def Reset_E(self):
        return self.Set_E(False, 0, 0)
    
ultrasons = Class_Ultrasons()