from threading import Lock
from Constants import DIJKSTRA_MATCH

class Coordinate:
    home = [0, 0]
    def __init__(self):
        self.x = 0
        self.y = 0
        self.coo = [0, 0]
        self.MUT = Lock()
    
    def Write_Loc(self, X, Y):
        self.MUT.acquire()
        self.x = X
        self.y = Y
        self.coo = [X, Y]
        self.MUT.release()

coordinate = Coordinate()

def get_Dot_from_Bal(bal):
    return DIJKSTRA_MATCH[1, bal]

def get_Loc_from_Bal(bal):
    return (DIJKSTRA_MATCH[2, bal], DIJKSTRA_MATCH[3, bal])

def get_Bal_from_Dot(dot):
    for bal in DIJKSTRA_MATCH[0,: ]:
        if DIJKSTRA_MATCH[1, bal] == dot:
            return bal

def get_Loc_from_Dot(dot):
    for bal in DIJKSTRA_MATCH[0,: ]:
        if DIJKSTRA_MATCH[1, bal] == dot:
            return (DIJKSTRA_MATCH[2, bal], DIJKSTRA_MATCH[3, bal])

def get_Bal_from_Loc(loc):
    for bal in DIJKSTRA_MATCH[0,: ]:
        if (DIJKSTRA_MATCH[2, bal] == loc[0]) and (DIJKSTRA_MATCH[3, bal] == loc[1]):
            return bal

def get_Dot_from_Loc(loc):
    for bal in DIJKSTRA_MATCH[0,: ]:
        if (DIJKSTRA_MATCH[2, bal] == loc[0]) and (DIJKSTRA_MATCH[3, bal] == loc[1]):
            return DIJKSTRA_MATCH[1, bal]

if __name__ == '__main__':
    print(get_Bal_from_Loc([4, 12]))
    print(get_Dot_from_Loc([4, 12]))
    print(get_Bal_from_Dot(11))
    print(get_Loc_from_Dot(11))
    print(get_Dot_from_Bal(4))
    print(get_Loc_from_Bal(4))
