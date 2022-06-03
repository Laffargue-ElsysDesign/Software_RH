from signal import signal, SIGINT

############FPGA drivers imports#########
import Robot.holo32.lib.uart_driver
import Robot.FPGA.lib.imu_driver
import Robot.FPGA.lib.rfid_driver
import Robot.FPGA.lib.ronde_driver
import Robot.FPGA.lib.balise_driver
import Robot.FPGA.lib.dijkstra_driver
import Robot.FPGA.lib.ultrasons_driver

###########Threads Imports###############
#from Robot import IHM
from Robot.Detection import thread_detection
from Robot.EKF import thread_localisation
from Robot.ManualControl import thread_manual_control
from Robot.AutoControl import thread_auto_control
from Robot.Gestionnaire_mission import thread_gestionnaire
from Robot.Navigation import thread_Navigation
from Robot.Evitement import thread_evitement
from Robot.holo32.holo_uart_management import thread_holo32

##########Overlay to program on PL############
from Robot.Overlays.Overlay import overlay




#handler pour interrupt correctement 
def handler(signal_received, frame):
    #Handle any cleanup here. All threads are ended properly, one after the other
    thread_holo32.Interrupt()
    thread_holo32.join()
    print("HOLOCOM exited succesfully")
    thread_evitement.Interrupt()
    thread_evitement.join()
    print("Evitement exited succesfully")
    thread_localisation.Interrupt()
    thread_localisation.join()
    print("Localisation exited succesfully")
    thread_detection.Interrupt()
    thread_detection.join()
    print("Detection exited succesfully")
    thread_Navigation.Interrupt()
    thread_Navigation.join()
    print("Navigation stopped properly")
    thread_auto_control.Interrupt()
    thread_auto_control.join()
    print("AutoControl stopped properly")
    thread_manual_control.Interrupt()
    print("Press enter")
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
    overlay.download()
    #if overlay.is_loaded()==False:
    #    print("Loading Overlay..")
    #    overlay.download()
    
    
    #Start IHM
    #app.run(debug = True)

    #Start UART Comunication with robot
    #thread_holo = HUM.Holo_UART(overlay)

    ################Start all threads###################
    thread_holo32.start()
    #print("holo thread start")
    thread_localisation.start()
    #print("loc thread start")
    thread_Navigation.start()
    #print("nav thread start")
    thread_manual_control.start()
    #print("manual thread start")
    thread_auto_control.start()
    #print("auto thread start")
    thread_gestionnaire.start()
    #print("gestionnaire thread start")
    thread_detection.start()
    #print("detection thread start")
    thread_evitement.start()
    #print("detection thread start")

    
