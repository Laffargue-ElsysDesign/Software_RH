from threading import Thread
from time import sleep
import numpy as np

class Look(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.A= "Hello"

    def run(self):
        print(self.A)
    
class LookAgain(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.A= "World"

    def run(self):
        sleep(10)
        print(self.A)

if __name__ == '__main__':
    
    A = 370
    B = 180
    C = 1080

    print( A % 360, B - (B // 90)*90, C - (C // 360)*360)