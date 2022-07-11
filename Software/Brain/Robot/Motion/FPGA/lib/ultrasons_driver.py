from pynq import DefaultIP                      

class UltrasonsDriver(DefaultIP):
    def __init(self, description):
        super().__init(description=description)
        self.reset()
    bindto = ['elsys-design.com:user:Balise_reg:1.0'] #TBD
    
    def Enable(self):
        return 0 #TBD

    def Disable(self):
        return 0 #TBD

    def Read_N_Detection(self):
        return 0 #TBD

    def Read_NW_Detection(self):
        return 0 #TBD

    def Read_NE_Detection(self):
        return 0 #TBD

    def Read_W_Detection(self):
        return 0 #TBD

    def Read_E_Detection(self):
        return 0 #TBD

    def Read_ALL_Detection(self):
        return (self.Read_W_Detection(), self.Read_NW_Detection(), self.Read_N_Detection(), self.Read_NE_Detection(), self.Read_E_Detection()) #TBD

    def Read_N_Zone(self):
        return 0 #TBD

    def Read_NW_Zone(self):
        return 0 #TBD

    def Read_NE_Zone(self):
        return 0 #TBD

    def Read_W_Zone(self):
        return 0 #TBD

    def Read_E_Zone(self):
        return 0 #TBD

    def Read_ALL_Zone(self):
        return (self.Read_W_Zone(), self.Read_NW_Zone(), self.Read_N_Zone(), self.Read_NE_Zone(), self.Read_E_Zone()) #TBD

    def Read_N_Value(self):
        return 0 #TBD

    def Read_NW_Value(self):
        return 0 #TBD

    def Read_NE_Value(self):
        return 0 #TBD

    def Read_W_Value(self):
        return 0 #TBD

    def Read_E_Value(self):
        return 0 #TBD

    def Read_ALL_Value(self):
        return (self.Read_W_Value(), self.Read_NW_Value(), self.Read_N_Value(), self.Read_NE_Value(), self.Read_E_Value()) #TBD