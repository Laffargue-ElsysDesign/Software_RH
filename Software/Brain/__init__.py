from re import M
from signal import signal, SIGINT
#from Brain.Robot import IHM
#from pynq import Overlay
from Robot.ManualControl import thread_manual_control
from Robot.AutoControl import thread_auto_control
from Robot.Gestionnaire_mission import thread_gestionnaire
from Robot.Navigation import thread_Navigation

#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    thread_Navigation.Set_Interrupt()
    thread_Navigation.join()
    thread_manual_control.Set_Interrupt()
    thread_manual_control.join()
    thread_auto_control.Set_Interrupt()
    thread_auto_control.join()
    thread_gestionnaire.Set_Interrupt()
    thread_gestionnaire.join()

    #HUM.cmd_robot.speed_x=self.speed_x
    #HUM.cmd_robot.speed_y=self.speed_y
    #HUM.cmd_robot.speed_z=self.speed_z
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)



#app=Create_App()

if __name__ == '__main__':
    signal(SIGINT, handler)

    #global overlay
    #overlay=Overlay("./Robot/Motion/holo32/Overlays/UartComm/CorrectFiles/UartComm.bit", download=False)
    #if overlay.is_loaded()==False:
    #    overlay.download()
    
    #print('Bring up uart....')
    
    #Start IHM
    #app.run(debug = True)

    #Start UART Comunication with robot
    #thread_holo = HUM.Holo_UART(overlay)
    #thread_holo.start()

    thread_Navigation.start()

    thread_manual_control.start()
    
    thread_auto_control.start()
    
    thread_gestionnaire.start()


    
