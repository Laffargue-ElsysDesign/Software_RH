from threading import Thread
from Robot.Alerts import alerts
import Robot.Constants as cst
from Robot.Navigation import thread_Navigation as tn
from Robot.Alerts import Mgt
from time import sleep
from Robot.Motion.FPGA.dijkstra import Dijkstra
from Robot.Motion.Overlays.Overlay import overlay


class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mgt = Mgt()
        self.state = cst.HOME
        self.Navigation = tn
        self.interrupt = False

    def Set_Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()

    def Wait_Start(self):
        print("End of Auto_Control")
        while self.mgt.Check_Stop():
            self.mgt.Is_Waiting()
            sleep(0.1)
        self.mgt.Is_Not_Waiting()
        return 1

    def End_Navigation(self):
        if not self.Navigation.mgt.Check_Waiting():
            self.Navigation.mgt.Stop()
            while not self.Navigation.mgt.Check_Waiting():
                sleep(0.1)
        return 1
    
    def Start_Navigation(self, path):
        if path[0] != path[1]:
            self.Navigation.Set_Path(path)
            self.Navigation.mgt.Restart()
        else:
            self.Navigation.Set_Path([path[0]])
        return 0

    def run(self):
        #TBD
        dijkstra = Dijkstra(overlay)

        while not self.interrupt:
            #Wait until Auto Mode gets called
            self.Wait_Start()
            print("Start of Auto Control")
            #Continue until AutoMode gets shut down
            while not self.mgt.Check_Stop() and not self.interrupt:
                #print("Auto_Control")
                #Current_Loc = 0 #TBD

                #If battery Alert, got back home asap
                if alerts.Get_Battery_Alert():
                    print("Battery triggered")
                    self.End_Navigation()
                    #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    self.Start_Navigation(cst.LOC_HOME)
                    alerts.Reset_Battery_Alert()
                
                #If a new alert is triggeres, gets priority
                elif alerts.Get_Balise_Alert():
                    print("Balise Triggered")
                    self.End_Navigation()
                    #self.Alerts.Balise.MUT.acquire()
                    self.Start_Navigation(dijkstra.Compute(0, alerts.Get_Balise_Dot()))
                    alerts.Reset_Balise_Alert()
                    #self.Alerts.Balise.MUT.release()
                    alerts.Reset_Balise_Alert()

                elif alerts.Get_Ronde_Alert():
                    print("Ronde triggered")
                    if self.Navigation.mgt.Check_Waiting():
                        self.Start_Navigation(cst.LOC_HOME)
                    alerts.Reset_Ronde_Alert()


            self.End_Navigation() 


thread_auto_control = Auto_Control()