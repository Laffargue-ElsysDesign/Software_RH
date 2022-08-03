from threading import Thread
from Robot.Alerts import alerts, ultrasons
from Robot.FPGA.balise import Balises
from Robot.FPGA.battery import Battery
from Robot.FPGA.ronde import Ronde
from Robot.FPGA.ultrasons import Ultrasons

class Detection_Alert(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.interrupt = False
        self.balises = Balises()
        self.battery = Battery()
        self.ronde = Ronde()
        self.ultrasons = Ultrasons()
    
    def Set_Interrupt(self):
        self.interrupt = True

    ##This updates the class_ultrasounds so all datas are ready to be used
    def Manage_US(self):
        (W_det, NW_det, N_det, NE_det, E_det) = self.ultrasons.Check_US_Detection()
        (W_zone, NW_zone, N_zone, NE_zone, E_zone) = self.ultrasons.Check_US_Zone()
        (W_val, NW_val, N_val, NE_val, E_val) = self.ultrasons.Get_Values()

        ultrasons.Set_W(W_det, W_zone, W_val)
        
        ultrasons.Set_NW(NW_det, NW_zone, NW_val)
        
        ultrasons.Set_N(N_det, N_zone, N_val)
        
        ultrasons.Set_NE(NE_det, NE_zone, NE_val)
        
        ultrasons.Set_E(E_det, E_zone, E_val)
        
        return 0

    
    def run(self):
        while(not self.interrupt):
            
            ##Update for Battery
            if self.battery.Check():
                alerts.Set_Battery_Alert()
            else:
                alerts.Reset_Battery_Alert()
            
            ##Update for balise
            new, dot = self.balises.Check_Balise()
            if new:
                if not (dot == alerts.Get_Balise_Dot()):
                    alerts.Set_Balise_Alert(dot)
            
            ##Update for Ronde
            if self.ronde.Check():
                alerts.Set_Ronde_Alert()
            else:
                alerts.Reset_Ronde_Alert()
            
            ##Update for utrasounds
            self.Manage_US()

thread_detection = Detection_Alert()
            

