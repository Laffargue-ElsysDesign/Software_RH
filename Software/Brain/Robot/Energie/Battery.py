from threading import Thread, Lock

class Battery_Alert:
    def __init__(self):
        self.alert = False
        self.MUT = Lock()
    
    def New_Alert(self):
        self.MUT.acquire()
        self.alert = True
        self.MUT.release()

    def End_Alert(self):
        self.MUT.acquire()
        self.alert = False
        self.MUT.release()
    
class Charging:
    def __init__(self):
        self.isPlug = False
        self.MUT = Lock()

alert=Battery_Alert()
charge=Charging()