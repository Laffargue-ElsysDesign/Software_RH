# Alerts.py

#  Created on: June 2 2022
#      Author: Lenny Laffargue
#

####### Python pakages imports #######
from threading import Lock

######### Data imports ############
import Robot.Permanent.Constants as cst

class State_NFC():
    def __init__(self):
        self.new = False
        self.data_valid = False
        self.point = 0 
        self.position = 0
        self.last_dot = 0
        self.MUT = Lock()

    def Get_New(self):
        self.MUT.acquire()
        alert = self.new
        self.MUT.release()
        return alert

    def Get_Tag(self):
        self.MUT.acquire()
        valid = self.data_valid
        point = self.point
        position = self.position
        self.MUT.release()
        return (valid, point, position)
    
    def Get_LastDot(self):
        self.MUT.acquire()
        point = self.last_dot
        self.MUT.release()
        return point
    
    def Set_New(self):
        self.MUT.acquire()
        self.new = True
        self.data_valid = False
        self.point = 0
        self.position = 0
        self.MUT.release()
        return 1
    
    def Set_Tag(self, point, position):
        self.MUT.acquire()
        self.new = True
        self.data_valid = True
        self.point = point
        self.positon = position
        self.last_dot = point
        print("New dot registered",point, position)
        self.MUT.release()
        return 1

    def Reset(self):
        self.MUT.acquire()
        self.new = False
        self.data_valid = False
        self.point = 0
        self.position = 0
        self.MUT.release()
        return 1

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
        dot = self.dot
        self.MUT.release()
        return dot
    
    def Set_Balise(self, dot):
        self.MUT.acquire()
        self.new = True
        self.dot = dot
        self.MUT.release()
        return 1

    def Reset(self):
        self.MUT.acquire()
        self.new = False
        self.dot = cst.dots.DOT_NOWHERE
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
        self.NFC = State_NFC()

    def Get_NFC_Alert(self):
        return self.NFC.Get_New()
    
    def Get_NFC_Tag(self):
        return self.NFC.Get_Tag()
    
    def Get_NFC_LastDot(self):
        return self.NFC.Get_LastDot()

    def Set_NFC_New(self):
        return self.NFC.Set_New()
    
    def Set_NFC_Alert(self, point, position):
        return self.NFC.Set_Tag(point, position)
    
    def Reset_Tag_Alert(self):
        return self.NFC.Reset()
    
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

    def Set_Balise_Alert(self, dot):
        return self.balise.Set_Balise(dot)
    
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
class Mgt():
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