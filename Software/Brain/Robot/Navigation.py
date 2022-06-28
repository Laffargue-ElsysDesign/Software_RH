from threading import Thread, Lock
from Robot.IHM.interface import cst

def Dijkstra(End):
    pass #TBD

class mgt():
    def __init__(self):
        self.Stop = True
        self.Waiting = True

def Compute_Angle(point):
    return 0 #TBD

def Rotate(angle):
    pass #TBD



def Correct():
    pass #TBD

class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = [0, 0] #TBD
        self.Mgt = mgt()
        self.MUT = Lock()

    def Get_to_Point(self, point):
        Angle = Compute_Angle(point)
        while Angle > 2: #TBD
            Rotate(Angle)
            Angle=Compute_Angle(point)
            if self.Mgt.Stop:
                return
            self.Froward(point)
            if self.Mgt.Stop:
                return
            Correct()

    def Froward(self):
        pass #TBD     

    def Wait_Start(self):
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
            #print("Navigate Stopped")
        self.Mgt.Waiting = False
        return

    def run(self):
        while True:
            self.Wait_Start()
            while not self.Mgt.Stop:
                print("Navigating")
                for i in self.path:
                    #self.Get_to_Point(i)
                    if self.Mgt.Stop:
                        break
                #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    #self.MUT.acquire()
                    #self.path = Dijkstra(cst.Home)
                    #self.MUT.release()
                #else:
                    #self.Mgt.Stop = True
                    
