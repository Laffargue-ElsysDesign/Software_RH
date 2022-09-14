# battery_driver.py

#  Created on: July 8 2022
#      Author: Isabelle Van Leeuwen and Lenny Laffargue
#

######## PYNQ import #########
from pynq import DefaultIP                      

class BatteryDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Read_State(self):
        return 0 #TBD

