from threading import Lock

class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.MUT = Lock()
    
    def Write_Loc(self, X, Y):
        self.MUT.acquire()
        self.x = X
        self.y = Y
        self.MUT.release()

coordinate = Coordinate()