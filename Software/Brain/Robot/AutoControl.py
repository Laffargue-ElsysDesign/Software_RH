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
            #Wait until Auto Mode gets called
            self.Wait_Start()

            #Continue until AutoMode gets shut down
            while not self.Mgt.Stop:

                Current_Loc = 0 #TBD

                #If battery Alert, got back home asap
                if self.Alerts.Battery:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                        self.Navigation.MUT.acquire()
                        self.Navigation.path = Dijkstra(cst.Home)
                        self.Navigation.MUT.release()
                        self.Navigation.Mgt.Stop = False
                
                #If a new alert is triggeres, gets treated first
                if self.Alerts.Balise.New:
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            pass
                    self.Alerts.Balise.MUT.acquire()
                    self.Navigation.MUT.acquire()
                    self.Navigation.path = Dijkstra(self.Alerts.Balise.Loc)
                    self.Navigation.MUT.release()
                    self.Alerts.Balise.MUT.release()
                    self.Navigation.Mgt.Stop = False

            self.Navigation.Mgt.Stop = True
            while not self.Navigation.Mgt.Waiting:
                pass