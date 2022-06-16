from time import sleep, time
from threading import Thread, Lock
from signal import signal, SIGINT

from IHM.interface import cst
from Navigation import Navigation, Dijkstra, mgt

class Balise ():
    def __init__(self):
        self.New = False
        self.Loc = 0 #TBD
        self.MUT = Lock()

class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.Mgt = mgt()
        self.Battery = False
        self.Ronde = False
        self.Balise = Balise()
        self.state = cst.HOME
        self.Navigation = Navigation()

    def run(self):
        #TBD
        self.Navigation.start()
        self.Mgt.Stop = False
        self.Mgt.Waiting = False
        while True:
            while self.Mgt.Stop:
                self.Mgt.Waiting = True
            self.Mgt.Waiting = False
            while not self.Mgt.Stop:

                Current_Loc = 0 #TBD

                if self.Battery:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                        self.Navigation.path = Dijkstra(cst.Home, Current_Loc)
                        self.Navigation.Mgt.Stop = False
                        
                if self.Balise.New:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                    self.Balise.MUT.acquire()
                    self.Navigation.path = Dijkstra(self.Balise.Loc, Current_Loc)
                    self.Balise.MUT.release()
                    self.Navigation.Mgt.Stop = False

            self.Navigation.Mgt.Stop = True
            while not self.Navigation.Mgt.Waiting:
                pass