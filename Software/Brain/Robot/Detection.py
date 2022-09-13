##########Classic imports#########
from threading import Thread
from time import sleep

#########Sensor imports###########
from Robot.FPGA.balise import Balises
#from Robot.FPGA.battery import Battery
from Robot.FPGA.ronde import Ronde
from Robot.FPGA.ultrasons import Ultrasons
from Robot.FPGA.imu import IMU
from Robot.FPGA.rfid import RFID

######Overlay programmed en PL#####
from Robot.Overlays.Overlay import overlay

########Global variables#########
from Robot.EKF import imu_data
from Robot.Alerts import alerts, ultrasons

############Function used#############
from Robot.Localisation import Get_Dot_from_ID


class Detection_Alert(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.interrupt = False
        self.balises = Balises(overlay)
        #self.battery = Battery(overlay)
        self.ronde = Ronde(overlay)
        self.rfid = RFID(overlay)
        self.ultrason = Ultrasons(overlay)
        
        self.imu = IMU(overlay)
    
    def Interrupt(self):
        self.interrupt = True

    ##This updates the class_ultrasounds so all datas are ready to be used
    def Manage_US(self):
        (W_det, NW_det, N_det, NE_det, E_det) = self.ultrason.Check_US_Detection()
        (W_zone, NW_zone, N_zone, NE_zone, E_zone) = self.ultrason.Check_US_Zone()
        (W_val, NW_val, N_val, NE_val, E_val) = self.ultrason.Get_Values()
        #print(W_det, NW_det, N_det, NE_det, E_det)
        ultrasons.Set_W(W_det, W_zone, W_val)
        
        ultrasons.Set_NW(NW_det, NW_zone, NW_val)
        
        ultrasons.Set_N(N_det, N_zone, N_val)
        
        ultrasons.Set_NE(NE_det, NE_zone, NE_val)
        
        ultrasons.Set_E(E_det, E_zone, E_val)
        
        return 0

    
    def run(self):

        self.ronde.Set_2_hour()
        self.ultrason.Enable()
        while(not self.interrupt):
            
            ##Update for Battery
            #if self.battery.Check():
            #    alerts.Set_Battery_Alert()
            #else:
            #    alerts.Reset_Battery_Alert()
            
            ##Update for balise
            new_balise, id = self.balises.Check_Balise()
            if new_balise:
                print("New balise id:" ,id)
                if not (id == alerts.Get_Balise_Dot()):
                    alerts.Set_Balise_Alert(Get_Dot_from_ID(id))
            
            ##Update for Ronde
            if self.ronde.Check():
                alerts.Set_Ronde_Alert()
            
            #Update for RFID
            new_rfid = self.rfid.Check_RFID()
            #print(new_rfid)
            if new_rfid:
                #print("RFID_Detected")
                alerts.Set_NFC_New()
                #print("Waiting for data")
                (point, position) = self.rfid.Read_Data()
                if not (point == 0 and position ==0):
                    alerts.Set_NFC_Alert(point,  position)
                #print("New Tag: ", point, " ", position)
            
            ##Update for utrasounds
            self.Manage_US()

            #Update IMU
            data = self.imu.Get_Raw_Data()
            imu_data.Write(data[0], data[1], data[5])
            #print(self.data[0], " ", self.data[1], " ", self.data[2], " ", self.data[3], " ", self.data[4], " ", self.data[5], " ", self.data[6], " ", self.data[7], " ", self.data[8], " ", odometry.speed_x, " ", odometry.speed_y, " ", odometry.speed_z)
            
            sleep(0.1)
        self.ultrason.Disable()

thread_detection = Detection_Alert()
            

