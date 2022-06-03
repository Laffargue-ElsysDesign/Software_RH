from threading import Thread
from Robot.Alerts import alerts, ultrasons
#from Robot.FPGA.balise import Balises
#from Robot.FPGA.battery import Battery
#from Robot.FPGA.ronde import Ronde
#from Robot.FPGA.ultrasons import Ultrasons
from Robot.FPGA.imu import IMU
from Robot.FPGA.rfid import RFID
from Robot.holo32.holo_uart_management import odometry
from Robot.Overlays.Overlay import overlay
from Robot.EKF import imu_data
from time import sleep

class Detection_Alert(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.interrupt = False
        #self.balises = Balises(overlay)
        #self.battery = Battery(overlay)
        #self.ronde = Ronde(overlay)
        self.rfid = RFID(overlay)
        #self.ultrasons = Ultrasons(overlay)
        
        self.imu = IMU(overlay)
    
    def Interrupt(self):
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
            #if self.battery.Check():
            #    alerts.Set_Battery_Alert()
            #else:
            #    alerts.Reset_Battery_Alert()
            
            ##Update for balise
            #new_balise, dot = self.balises.Check_Balise()
            #if new_balise:
            #    if not (dot == alerts.Get_Balise_Dot()):
            #        alerts.Set_Balise_Alert(dot)
            
            ##Update for Ronde
            #if self.ronde.Check():
            #    alerts.Set_Ronde_Alert()
            
            #Update for RFID
            new_rfid = self.rfid.Check_RFID()
            #print(new_rfid)
            if new_rfid:
                print("RFID_Detected")
                alerts.Set_NFC_New()
                print("Waiting for data")
                (point, position) = self.rfid.Read_Data()
                alerts.Set_NFC_Alert(point,  position)
                print("New Tag: ", point, " ", position)
            
            ##Update for utrasounds
            #self.Manage_US()

            #Update IMU
            data = self.imu.Get_Raw_Data()
            imu_data.Write(data[0], data[1], data[5])
            #print(self.data[0], " ", self.data[1], " ", self.data[2], " ", self.data[3], " ", self.data[4], " ", self.data[5], " ", self.data[6], " ", self.data[7], " ", self.data[8], " ", odometry.speed_x, " ", odometry.speed_y, " ", odometry.speed_z)
            
            sleep(0.1)

thread_detection = Detection_Alert()
            

