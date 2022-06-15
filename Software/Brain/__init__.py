import Robot.Motion.holo32.holo_uart_management as HUM 
from time import sleep, time
from threading import Thread, Lock
from signal import signal, SIGINT
from Software.Brain.Robot import IHM
from pynq import Overlay
from Robot.IHM.interface import mode
from Robot.IHM import Create_App
from Robot.Gestionnaire_mission import Gestionnnaire_Mission
from Test_ManualControl import Keyboard_Read, IHM_Read

#handler pour interrupt correctement 
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)



app=Create_App()

if __name__ == '__main__':
    signal(SIGINT, handler)

    global overlay
    overlay=Overlay("../bitstream/Test_3.bit", download=False)
    if overlay.is_loaded()==False:
        overlay.download()
    
    print('Bring up uart....')
    
    #Start IHM
    app.run(debug = True)

    #Start UART Comunication with robot
    thread_holo = HUM.Holo_UART(overlay)
    thread_holo.start()

    #Threads for Keyboard or IHM test
    thread_keyboard = Keyboard_Read()
    thread_keyboard.start()

    thread_keyboard = IHM_Read()
    thread_keyboard.start()

    #Decision making Thread, will replace IHM and debug threads
    thread_gestionnaire = Gestionnnaire_Mission()
    thread_gestionnaire.start()


    
