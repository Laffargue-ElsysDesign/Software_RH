from pynq import DefaultIP

OFFSET_RESET = 0x00
OFFSET_READ_STATE = 0x04
OFFSET_CONFIG_SEC = 0x08                  
OFFSET_CONFIG_COUNT = 0x0C

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

    def Config_sec(self):
        self.write(OFFSET_CONFIG_SEC, 1)

    def Config_min(self):
        self.write(OFFSET_CONFIG_SEC, 0)
    
    def Config_Count(self, count):
        self.write(OFFSET_CONFIG_COUNT, count)

    def Config_Timer(self, seconds, count):
        self.write(OFFSET_RESET, 1)

        if seconds:
            self.Config_sec()
        else:
            self.Config_min()

        self.Config_Count(count)
        self.write(OFFSET_RESET, 0)
        return 1