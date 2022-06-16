from threading import Thread
from time import sleep

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
    threadA = Look()
    threadB = LookAgain()
    threadB.start()
    threadA.start()
    threadB.join()