from time import sleep, time
from threading import Thread, Lock
from signal import signal, SIGINT

import Motion.holo32.holo_uart_management as HUM 

class Auto_Control(Thread):
    def __init__(self):
            Thread.__init__(self)

    def run(self):
        pass #TBD

