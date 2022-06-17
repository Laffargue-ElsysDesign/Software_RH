from threading import Thread
from Alerts import Alerts
from IHM.interface import cst
from Navigation import Navigation, Dijkstra, mgt



class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.Mgt = mgt()
        self.Alerts = Alerts()
        self.state = cst.HOME
        self.Navigation = Navigation()

    def Wait_Start(self):
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
        self.Mgt.Waiting = False
        return

    def run(self):
        #TBD
        self.Navigation.start()
        self.Mgt.Stop = False
        self.Mgt.Waiting = False
        while True:
            self.Wait_Start()
            while not self.Mgt.Stop:

                Current_Loc = 0 #TBD

                if self.Alerts.Battery:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                        self.Navigation.path = Dijkstra(cst.Home, Current_Loc)
                        self.Navigation.Mgt.Stop = False
                        
                if self.Alerts.Balise.New:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                    self.Alerts.Balise.MUT.acquire()
                    self.Navigation.path = Dijkstra(self.Alerts.Balise.Loc, Current_Loc)
                    self.Alerts.Balise.MUT.release()
                    self.Navigation.Mgt.Stop = False

            self.Navigation.Mgt.Stop = True
            while not self.Navigation.Mgt.Waiting:
                pass