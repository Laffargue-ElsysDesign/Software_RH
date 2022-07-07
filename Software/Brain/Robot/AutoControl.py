from threading import Thread
from Robot.Alerts import alerts
import Robot.Constants as cst
from Robot.Navigation import thread_Navigation as tn
from Robot.Alerts import mgt
from time import sleep



class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.Mgt = mgt()
        self.state = cst.HOME
        self.Navigation = tn
        self.Interrupt = False

    def Wait_Start(self):
        print("End of Auto_Control")
        while self.Mgt.Stop:
            self.Mgt.Waiting = True
            #print("Auto Stopped")
        self.Mgt.Waiting = False

        return

    def End_Navigation(self):
        if not self.Navigation.Mgt.Waiting:
            self.Navigation.Mgt.Stop = True
            while not self.Navigation.Mgt.Waiting:
                sleep(0.01)
        return 1
    
    def Start_Navigation(self, path):
        self.Navigation.MUT.acquire()
        self.Navigation.path = path
        self.Navigation.MUT.release()
        self.Navigation.Mgt.Stop = False
        return 0

    def run(self):
        #TBD

        while not self.Interrupt:
            #Wait until Auto Mode gets called
            self.Wait_Start()
            print("Start of Auto Control")
            #Continue until AutoMode gets shut down
            while not self.Mgt.Stop and not self.Interrupt:
                #print("Auto_Control")
                #Current_Loc = 0 #TBD

                #If battery Alert, got back home asap
                if alerts.Battery:
                    print("Battery triggered")
                    self.End_Navigation()
                    #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    self.Start_Navigation(cst.LOC_HOME)
                    alerts.Battery = False
                
                #If a new alert is triggeres, gets priority
                elif alerts.Balise.New:
                    print("Balise Triggered")
                    self.End_Navigation()
                    #self.Alerts.Balise.MUT.acquire()
                    self.Start_Navigation(cst.LOC_HOME)
                    #self.Alerts.Balise.MUT.release()
                    alerts.Balise.New = False

                elif alerts.Ronde.New:
                    print("Ronde triggered")
                    if self.Navigation.Mgt.Waiting:
                        self.Start_Navigation(cst.LOC_HOME)
                    alerts.Ronde.New = False


            self.End_Navigation() 


thread_auto_control = Auto_Control()