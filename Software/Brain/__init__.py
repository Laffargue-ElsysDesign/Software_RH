from signal import signal, SIGINT
#from Brain.Robot import IHM
#from pynq import Overlay
from Robot.ManualControl import thread_manual_control
from Robot.AutoControl import thread_auto_control
from Robot.Gestionnaire_mission import thread_gestionnaire
from Robot.Navigation import thread_Navigation
from Robot.Motion.Overlays.Overlay import overlay
import Robot.Motion.holo32.holo_uart_management as HUM 

#from Robot.Detection import thread_detection

#handler pour interrupt correctement 
def handler(signal_received, frame):
    #Handle any cleanup here. All threads are ended properly, one after the other
    #thread_detection.Set_Interrupt()
    #thread_detection.join()
    print("Trying to exit")
    thread_Navigation.Interrupt()
    thread_Navigation.join()
    print("Navigation stopped properly")
    thread_auto_control.Interrupt()
    thread_auto_control.join()
    print("AutoControl stopped properly")
    thread_manual_control.Interrupt()
    print("Press i and enter")
    thread_manual_control.join()
    print("ManualControl stopped properly")
    thread_gestionnaire.Interrupt()
    thread_gestionnaire.join()
    print("Gestionnaire stopped properly")

    #HUM.cmd_robot.Set_Speed(0, 0, 0)
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)



#app=Create_App()

if __name__ == '__main__':
    signal(SIGINT, handler)

    if overlay.is_loaded()==False:
        print("Loading Overlay..")
        overlay.download()
    
    
    #Start IHM
    #app.run(debug = True)

    #Start UART Comunication with robot
    thread_holo = HUM.Holo_UART(overlay)

    ################Start all threads###################
    thread_holo.start()
    
    thread_Navigation.start()

    thread_manual_control.start()
    
    thread_auto_control.start()
    
    thread_gestionnaire.start()

    #thread_detection.start()


    
