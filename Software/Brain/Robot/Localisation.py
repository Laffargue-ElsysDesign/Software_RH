from threading import Lock
from Robot.Permanent.Constants import ROOM_NFC_MATCH, DOT_POSITION_TO_X_MATCH, DOT_POSITION_TO_Y_MATCH
from Robot.Permanent.Map import ARC_MAP
from Robot.EKF import EKF

class Coordinate:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

        self.MUT = Lock()
    
    def Write_Loc(self, X, Y, angle):
        self.MUT.acquire()
        self.x = X
        self.y = Y
        self.angle = 0
        self.MUT.release()

    def Get_Angle(self):
        self.MUT.acquire()
        angle = self.angle
        self.MUT.release()
        return angle

coordinate = Coordinate()

thread_localisation = EKF()

def get_Dot_from_Bal(bal):
    return ROOM_NFC_MATCH[1, bal]

def get_Bal_from_Dot(dot):
    for bal in ROOM_NFC_MATCH[0,: ]:
        if ROOM_NFC_MATCH[1, bal] == dot:
            return bal

def Get_Loc_from_Dot(point, position):
    return (DOT_POSITION_TO_X_MATCH[point, position], DOT_POSITION_TO_Y_MATCH[point, position])

def Get_Orientation(start_point, end_point):
    return (ARC_MAP[start_point, end_point])
    

if __name__ == '__main__':
    print(get_Bal_from_Dot([4, 12]))
    #print(get_Dot_from_Loc([4, 12]))
    #print(get_Bal_from_Dot(11))
    #print(get_Loc_from_Dot(11))
    #print(get_Dot_from_Bal(4))
    #print(get_Loc_from_Bal(4))


