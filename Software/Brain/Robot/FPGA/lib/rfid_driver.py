from pynq import DefaultIP
from signal import signal, SIGINT
from time import sleep                   

class BaliseDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:rfid:1.0']
    
    def Read_State(self):
        state = self.read()
        return state
        
    def Read_Tag(self, timeout = 1):
        Tag = self.read()
        return Tag 
    
    def Reset(self):
        while self.Read_State():
            self.write()
            sleep(0.1)
        self.write()
        return 1

    def Read_Rfid(self):
        Tag = 0
        New = False
        if (self.Read_State() == 1):
            New = True
            Tag = self.Read_Tag()
            self.Reset()
        return (New, Tag)