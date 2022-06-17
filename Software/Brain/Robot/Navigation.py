from threading import Thread

def Dijkstra(Start, End):
    pass #TBD

class mgt():
    def __init__(self):
        self.Stop = False
        self.Waiting = False

def Compute_Angle(point):
    return 0 #TBD

def Rotate(angle):
    pass #TBD



def Correct():
    pass #TBD

class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = 0 #TBD
        self.Mgt = mgt()

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

    def run(self):
        self.Mgt.Stop = False
        self.Mgt.Waiting = False
        while True:
            while self.Mgt.Stop:
                self.Mgt.Waiting = True
            self.Mgt.Waiting = False
            while not self.Mgt.Stop:
                for i in self.path:
                    self.Get_to_Point(i)
                    if self.Mgt.Stop:
                        break
                