from threading import Thread, Lock
import Robot.Constants as cst
from time import sleep, time
from Robot.Alerts import mgt

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Navigation Exiting gracefully')
    exit(0)

def Dijkstra(End):
    pass #TBD

def Compute_Angle(point):
    return 0 #TBD

def Rotate(angle):
    pass #TBD


def Correct():
    pass #TBD

class Navigation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.path = [0, 0] #TBD
        self.Mgt = mgt()
        self.MUT = Lock()
        self.Interrupt = False

    def Set_Path(self, path):
        self.MUT.acquire()
        self.path = path
        self.MUT.release()

    def Set_Interrupt(self):
        self.Interrupt = True

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

    def Wait_Start(self):
        print("End of navigation")
        while self.Mgt.Check_Stop():
            self.Mgt.Is_Waiting()
        self.Mgt.Is_Not_Waiting()
        return

    def run(self):
        while not self.Interrupt:
            self.Wait_Start()
            print("Start of Navigation")
            T = time()
            while not self.Mgt.Check_Stop() and not self.Interrupt:
                sleep(1)
                if time() > (T + 10):
                    self.Mgt.Stop()
                #for i in self.path:
                    #self.Get_to_Point(i)
                    #if self.Mgt.Stop:
                        #break
                #if not cst.Home: #TBD: if not localisation = home at the end of the path then go home.
                    #self.MUT.acquire()
                    #self.path = Dijkstra(cst.Home)
                    #self.MUT.release()
                #else:
                    #self.Mgt.Stop = True
                    
thread_Navigation = Navigation()