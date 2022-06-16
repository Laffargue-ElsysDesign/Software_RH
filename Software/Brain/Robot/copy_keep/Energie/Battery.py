from threading import Thread, Lock

class Battery_Alert:
    def __init__(self):
        self.alert = False
        self.isPlug = False
        self.MUT = Lock()
    
    def New_Alert(self):
        self.MUT.acquire()
        self.alert = True
        self.MUT.release()

    def End_Alert(self):
        self.MUT.acquire()
        self.alert = False
        self.MUT.release()

    def is_Alert(self):
        self.MUT.acquire()
        output= self.alert
        self.MUT.release()
        return output

alert_battery=Battery_Alert()