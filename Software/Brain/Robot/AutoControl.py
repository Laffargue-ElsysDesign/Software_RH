from threading import Thread
from Robot.Alerts import alerts
import Robot.Permanent.Constants as cst
from Robot.Navigation import thread_Navigation as tn
from Robot.Alerts import Mgt
from time import sleep
from Robot.FPGA.dijkstra import Dijkstra
from Robot.Overlays.Overlay import overlay


class Auto_Control(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mgt = Mgt()
        self.Navigation = tn
        self.interrupt = False
        self.balise_trig = False

    def Interrupt(self):
        self.interrupt = True
        self.mgt.Stop()

    def Start_Balise_Alert(self, path):
        self.End_Navigation()
        self.balise_trig = True
        self.Start_Navigation(path)

    def Wait_Start(self):
        print("End of Auto_Control")
        while self.mgt.Check_Stop() and not self.interrupt:
            self.mgt.Is_Waiting()
            sleep(0.1)
            #print("Auto Waiting..")
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
            print("path nagation: ", path)
            self.Navigation.Set_Path(path)
            self.Navigation.mgt.Restart()
            while self.Navigation.mgt.Check_Waiting():
                sleep(0.1)
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

                #If battery Alert, get back home asap
                if alerts.Get_Battery_Alert():
                    #print("Battery triggered")
                    self.balise_trig = False
                    self.End_Navigation()
                    self.Start_Navigation(dijkstra.Compute(alerts.Get_NFC_LastDot(), cst.Room.STAGIAIRE))
                    alerts.Reset_Battery_Alert()
                
                #If a new alert is triggereg
                elif alerts.Get_Balise_Alert():
                    print("Balise Triggered")


                     
                    if not self.balise_trig:
                        print("starting")
                        self.Start_Balise_Alert(dijkstra.Compute(alerts.Get_NFC_LastDot(), int(alerts.Get_Balise_Dot())))
                    alerts.Reset_Balise_Alert()
                    
                    #self.Alerts.Balise.MUT.acquire()
                    
                    #alerts.Reset_Balise_Alert()
                    #self.Alerts.Balise.MUT.release()

                elif self.balise_trig:
                    if self.Navigation.mgt.Check_Waiting():
                        self.Start_Navigation(dijkstra.Compute(alerts.Get_NFC_LastDot(), cst.NFC_Dot.DOT_CHARGE))
                        self.balise_trig = False

                elif alerts.Get_Ronde_Alert():
                    print("Ronde triggered")
                    if self.Navigation.mgt.Check_Waiting():
                        self.Start_Navigation(dijkstra.Compute(alerts.Get_NFC_LastDot(), cst.Room.STAGIAIRE))
                    alerts.Reset_Ronde_Alert()
                    
            if not self.interrupt:
                self.End_Navigation() 


thread_auto_control = Auto_Control()