from pynq import DefaultIP
from signal import signal, SIGINT
from time import sleep

import time

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04
OFFSET_READ_BALISE = 0x08
MASK_BALISE = 0x0F                      

class BaliseDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise:1.0']
    
    def Read_State(self):
        state = self.read(OFFSET_READ_STATE) & 1
        return state
        
    def Read_Loc(self, timeout = 1):
        Loc = self.read(OFFSET_READ_BALISE) & MASK_BALISE
        return Loc 
    
    def Reset(self):
        while self.Read_State():
            self.write(OFFSET_RESET, 1)
            sleep(0.1)
        self.write(OFFSET_RESET, 0)
        return 1

    def Read_Balise(self):
        Loc = 0
        New = False
        if (self.Read_State() == 1):
            New = True
            Loc = self.Read_Loc()
            self.Reset()
        return (New, Loc)