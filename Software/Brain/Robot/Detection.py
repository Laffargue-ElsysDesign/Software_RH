from threading import Thread, Lock

class Detection_Alert(Thread):
    def __init__(self):
        Thread.__init__(self)
        