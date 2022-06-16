from threading import Thread

def Dijkstra(Start, End):
    pass #TBD

class mgt():
    def __init__(self):
        self.Stop = False
        self.Waiting = False



class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = 0 #TBD
        self.Mgt = mgt()

    def run(self):
        self.Mgt.Stop = False
        self.Mgt.Waiting = False
        while True:
            while self.Mgt.Stop:
                self.Mgt.Waiting = True
            self.Mgt.Waiting = False
            while not self.Mgt.Stop:
                pass