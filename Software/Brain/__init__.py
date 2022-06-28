from time import sleep, time
from threading import Thread, Lock
from signal import signal, SIGINT
#from Brain.Robot import IHM
#from pynq import Overlay
from Robot.IHM.interface import mode
from Robot.IHM import Create_App
from Robot.Gestionnaire_mission import Gestionnnaire_Mission
from Robot.ManualControl import Keyboard_Read, IHM_Read

#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
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

    #Decision making Thread, will replace IHM and debug threads
    thread_gestionnaire = Gestionnnaire_Mission()
    thread_gestionnaire.start()


    
