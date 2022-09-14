# ultrasons_driver.py

#  Created on: July 8 2022
#      Author: Isabelle Van Leeuwen and Lenny Laffargue
#

########## Python packages imports ##########
from signal import signal,SIGINT

######## PYNQ import #########
from pynq import DefaultIP, Overlay

OFFSET_WRITE_ENABLE = 0x00

OFFSET_READ_N = 0x04
OFFSET_READ_NW = 0x08
OFFSET_READ_NE = 0x0C
OFFSET_READ_W = 0x14
OFFSET_READ_E = 0x10

MASQUE_OBJ = 0x10
MASQUE_ZONE1 = 0x01
MASQUE_ZONE2 = 0x02
MASQUE_ZONE3 = 0x04
MASQUE_DIST = 0xFF00

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)                       

class UltrasonsDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Ultrasons:1.0'] #TBD
    
    def Enable(self):
        self.write(OFFSET_WRITE_ENABLE, 1)
        return 1

    def Disable(self):
        self.write(OFFSET_WRITE_ENABLE, 0)
        return 0

    def Read_N_Detection(self):
        obj = (self.read(OFFSET_READ_N) & MASQUE_OBJ)>>4
        return obj

    def Read_NW_Detection(self):
        obj = (self.read(OFFSET_READ_NW) & MASQUE_OBJ)>>4
        return obj

    def Read_NE_Detection(self):
        obj = (self.read(OFFSET_READ_NE) & MASQUE_OBJ)>>4
        return obj

    def Read_W_Detection(self):
        obj = (self.read(OFFSET_READ_W) & MASQUE_OBJ)>>4
        return obj

    def Read_E_Detection(self):
        obj = (self.read(OFFSET_READ_E) & MASQUE_OBJ)>>4
        return obj

    def Read_ALL_Detection(self):
        return (self.Read_W_Detection(), self.Read_NW_Detection(), self.Read_N_Detection(), self.Read_NE_Detection(), self.Read_E_Detection()) #TBD

    def Read_N_Zone(self):
        if (self.read(OFFSET_READ_N) & MASQUE_ZONE1) == 1 : 
            zone = 1
        elif (self.read(OFFSET_READ_N)& MASQUE_ZONE2)>>1  == 1 :
            zone = 2
        elif (self.read(OFFSET_READ_N) & MASQUE_ZONE3)>>2 == 1 :
            zone = 3
        else :
            zone = 0
        return zone

    def Read_NW_Zone(self):
        if (self.read(OFFSET_READ_NW) & MASQUE_ZONE1) == 1 : 
            zone = 1
        elif (self.read(OFFSET_READ_NW) & MASQUE_ZONE2)>>1 == 1 :
            zone = 2
        elif (self.read(OFFSET_READ_NW) & MASQUE_ZONE3)>>2 == 1 :
            zone = 3
        else :
            zone = 0
        return zone

    def Read_NE_Zone(self):
        if (self.read(OFFSET_READ_NE) & MASQUE_ZONE1) == 1 : 
            zone = 1
        elif (self.read(OFFSET_READ_NE) & MASQUE_ZONE2)>>1 == 1 :
            zone = 2
        elif (self.read(OFFSET_READ_NE) & MASQUE_ZONE3)>>2 == 1 :
            zone = 3
        else :
            zone = 0
        return zone

    def Read_W_Zone(self):
        if (self.read(OFFSET_READ_W) & MASQUE_ZONE1) == 1 : 
            zone = 1
        elif (self.read(OFFSET_READ_W) & MASQUE_ZONE2)>>1 == 1 :
            zone = 2
        elif (self.read(OFFSET_READ_W) & MASQUE_ZONE3)>>2 == 1 :
            zone = 3
        else :
            zone = 0
        return zone

    def Read_E_Zone(self):
        if (self.read(OFFSET_READ_E) & MASQUE_ZONE1) == 1 : 
            zone = 1
        elif (self.read(OFFSET_READ_E) & MASQUE_ZONE2)>>1 == 1 :
            zone = 2
        elif (self.read(OFFSET_READ_E)>>2 & MASQUE_ZONE3)>>2 == 1 :
            zone = 3
        else :
            zone = 0
        return zone

    def Read_ALL_Zone(self):
        return (self.Read_W_Zone(), self.Read_NW_Zone(), self.Read_N_Zone(), self.Read_NE_Zone(), self.Read_E_Zone()) #TBD

    def Read_N_Value(self):
        dist = (self.read(OFFSET_READ_N) & MASQUE_DIST)>>8
        return dist

    def Read_NW_Value(self):
        dist = (self.read(OFFSET_READ_NW) & MASQUE_DIST)>>8
        return dist

    def Read_NE_Value(self):
        dist = (self.read(OFFSET_READ_NE) & MASQUE_DIST)>>8
        return dist

    def Read_W_Value(self):
        dist = (self.read(OFFSET_READ_W) & MASQUE_DIST)>>8
        return dist

    def Read_E_Value(self):
        dist = (self.read(OFFSET_READ_E) & MASQUE_DIST)>>8
        return dist

    def Read_ALL_Value(self):
        return (self.Read_W_Value(), self.Read_NW_Value(), self.Read_N_Value(), self.Read_NE_Value(), self.Read_E_Value()) #TBD

   

class Ultrasons():
    def __init__(self, overlay):
        self.ultrasons = overlay.ultrasons_0 #TBD

    def Check_US_Detection(self): #TBD
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Detection()
        return W, NW, N, NE, E

    def Check_US_Zone(self): #TBD
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Zone()
        return W, NW, N, NE, E

    def Get_Values(self):
        (W, NW, N, NE, E) = self.ultrasons.Read_ALL_Value()
        return [W, NW, N, NE, E]

    def Enable(self):
        self.ultrasons.Enable()
        return 1

    def Disable(self):
        self.ultrasons.Disable()
        return 1

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Wrappers/Dijkstra_V2/Files/Dijkstra.bit")
    overlay.download()
    ultrasons = Ultrasons()
    
    try :
        if ultrasons.Check_US_State():
            print("Obstacle detected")
    except:
        print("Ronde Lecture failed")