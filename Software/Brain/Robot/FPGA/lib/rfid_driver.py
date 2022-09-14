# rfid_driver.py

#  Created on: July 8 2022
#      Author: Isabelle Van Leeuwen and Lenny Laffargue
#

########## Python packages imports ##########
from time import sleep

######## PYNQ import #########
from pynq import DefaultIP
                   

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04   
OFFSET_DATA_POSITION = 0x08
OFFSET_DATA_POINT = 0x0C   

MASQUE_DV = 0x2
MASQUE_Tag = 0x1F

class BaliseDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:RFID_reader:1.0']
    
    def Read_Tag_Detect(self):
        state = self.read(OFFSET_READ_STATE) & 1
        return state
    
    def Read_Tag_Data_Valid(self):
        state = self.read(OFFSET_READ_STATE) & MASQUE_DV
        return state
        
    def Read_Tag(self, timeout = 1):
        Point = self.read(OFFSET_DATA_POINT) & MASQUE_Tag
        Position = self.read(OFFSET_DATA_POSITION) & MASQUE_Tag
        return (Point,Position)  
    
    def Reset(self):
        while self.Read_Tag_Detect():
            self.write(OFFSET_RESET, 1)
            sleep(0.1)
        self.write(OFFSET_RESET, 0)
        return 1

    def Read_Rfid(self):
        Point = 0
        Position = 0
        New = False
        if (self.Read_Tag_Data_Valid() == 1):
            New = True
            (Point, Position) = self.Read_Tag()
            self.Reset()
        return (New, Point, Position)