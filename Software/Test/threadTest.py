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
    matrix = np.eye(3)
    for i in range(3):
        print(i)
    print(i)