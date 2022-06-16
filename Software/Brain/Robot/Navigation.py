from threading import Thread

def Dijkstra(Start, End):
    pass #TBD

class mgt():
    def __init__(self):
        self.Stop = False
        self.Waiting = False

def Compute_Angle(point):
    pass #TBD

def Rotate(angle)

class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = 0 #TBD
        self.Mgt = mgt()

    def Get_to_Point(self, point):
        Angle = Compute_Angle(Point)
        while Angle > 2: #TBD
            Rotate(Angle)
            Angle=Compute_Angle(point)
        
        

    def run(self):
        self.Mgt.Stop = False
        self.Mgt.Waiting = False
        while True:
            while self.Mgt.Stop:
                self.Mgt.Waiting = True
            self.Mgt.Waiting = False
            while not self.Mgt.Stop:
                for i in self.path:
                    self.Get_to_point(i)
                    if self.Mgt.Stop:
                        break
                