from threading import Thread
from Robot.Alerts import alerts
from Robot.IHM.interface import cst
from Robot.Navigation import Navigation, Dijkstra, mgt
from time import sleep



class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.Mgt = mgt()
        self.state = cst.HOME
        self.Navigation = Navigation()

    def Wait_Start(self):
        print("End of Auto_Control")
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
            #print("Auto Stopped")
        self.Mgt.Waiting = False

        return

    def run(self):
        #TBD
        self.Navigation.start()
        while True:
            #Wait until Auto Mode gets called
            self.Wait_Start()
            print("Start of Auto Control")
            #Continue until AutoMode gets shut down
            while not self.Mgt.Stop:
                #print("Auto_Control")
                #Current_Loc = 0 #TBD

                #If battery Alert, got back home asap
                if alerts.Battery:
                    print("Battery triggered")
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            sleep(0.01)
                    #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    self.Navigation.MUT.acquire()
                    self.Navigation.path = cst.Home
                    self.Navigation.MUT.release()
                    self.Navigation.Mgt.Stop = False
                    alerts.Battery = False
                
                #If a new alert is triggeres, gets priority
                elif alerts.Balise.New:
                    print("Balise Triggered")
                    if not self.Navigation.Mgt.Waiting:
                        self.Navigation.Mgt.Stop = True
                        while not self.Navigation.Mgt.Waiting:
                            sleep(0.01)
                    #self.Alerts.Balise.MUT.acquire()
                    self.Navigation.MUT.acquire()
                    self.Navigation.path = cst.Home
                    self.Navigation.MUT.release()
                    #self.Alerts.Balise.MUT.release()
                    self.Navigation.Mgt.Stop = False
                    alerts.Balise.New = False

                elif alerts.Ronde.New:
                    print("Ronde triggered")
                    if self.Navigation.Mgt.Waiting:
                        self.Navigation.MUT.acquire()
                        self.Navigation.path = cst.Home
                        self.Navigation.MUT.release()
                        self.Navigation.Mgt.Stop = False
                        alerts.Ronde.New = False
                        
            self.Navigation.Mgt.Stop = True
            while not self.Navigation.Mgt.Waiting:
                print(self.Navigation.Mgt.Waiting)