from pynq import DefaultIP

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04                      

class RondeDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Timer_ronde:1.0']
    
    def Read_State(self):
        state = self.read(OFFSET_READ_STATE) & 1
        return state

    def Reset(self):
        while ((self.read(OFFSET_READ_STATE) & 1) != 0):
            self.write(OFFSET_RESET, 1)
        self.write(OFFSET_RESET, 0)
        return 1

