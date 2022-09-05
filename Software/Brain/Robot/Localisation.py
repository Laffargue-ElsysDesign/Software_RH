from Robot.Permanent.Constants import ROOM_NFC_MATCH, DOT_POSITION_TO_X_MATCH, DOT_POSITION_TO_Y_MATCH
from Robot.Permanent.Map import ARC_MAP, BALISE_ID_TAG



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

def Get_Dot_from_ID(id):
    return BALISE_ID_TAG[1, id]

if __name__ == '__main__':
    print(get_Bal_from_Dot([4, 12]))
    #print(get_Dot_from_Loc([4, 12]))
    #print(get_Bal_from_Dot(11))
    #print(get_Loc_from_Dot(11))
    #print(get_Dot_from_Bal(4))
    #print(get_Loc_from_Bal(4))


