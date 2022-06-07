from threading import Thread
from IHM.interface import mode
from signal import signal, SIGINT
from IHM.interface import mode
from IHM import Create_App
import Motion.holo32.holo_uart_management as HUM 

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0)

class Gestionnnaire_Mission(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def Get_Trajectory(self, read_input):
        yes=1

    def run(self):
        prompt_counter = 10

app=Create_App()       
if __name__ == '__main__':
    signal(SIGINT, handler)

    global overlay
    overlay=Overlay("../bitstream/Test_3.bit", download=False)
    if overlay.is_loaded()==False:
        overlay.download()
    
    print('Bring up uart....')
    
    app.run(debug = True)

    thread_holo = HUM.Holo_UART(overlay)
    thread_holo.start()

    thread_gestionnaire = Gestionnnaire_Mission()
    thread_gestionnaire.start()

