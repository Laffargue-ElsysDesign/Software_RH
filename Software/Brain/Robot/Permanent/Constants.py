import numpy as np
from Robot.Permanent.Map import tags_loc as TL

#Mode
class Mode():
    AUTO = 0
    MANUAL = 1
modes = Mode()

#Mission en cours
class Mission():
    HOME = 0
    ALERT = 1
    RETURN = 2
    RONDE = 3
    IN_CHARGE = 4
    MANUAL = 5
missions = Mission()

#Etat batterie
class Battery_state():
    LOW_BATTERY = 0
    HIGH_BATTERY = 1
Battery_States = Battery_state()


#Ordres robot
class Orders():
    STOP=0
    NORTH=1
    SOUTH=2
    EAST=3
    WEST=4
    NORTH_WEST=5
    NORTH_EAST=6
    SOUTH_WEST=7
    SOUTH_EAST=8
    ROTATE_RIGHT=9
    ROTATE_LEFT=10
orders = Orders()

#Position Balises
class Room():
    NOWHERE = 0
    STAGIAIRE = 1
    MANAGER = 2
    PAUSE = 3
    REUNION = 4
    ENTREE = 5
    BUREAU = 6
    OPENSPACE = 7
rooms = Room()    

#Dijkstra dot
class NFC_Dot():
    DOT_CHARGE = 0
    DOT_STAGIAIRE = 1
    DOT_COULOIR_STAGIAIRE_1 = 2
    DOT_COULOIR_STAGIAIRE_2 = 3
    DOT_COULOIR_STAGIAIRE_2 = 4
    DOT_INTERSECTION_COULOIR = 5
    DOT_QUADRUPLE_INTERSECTION = 6
    DOT_MANAGER = 7
    DOT_PAUSE = 8
    DOT_REUNION = 9
    DOT_COULOIR_REUNION = 10
    DOT_ENTREE = 11
    DOT_COULOIR_BUREAU = 12
    DOT_BUREAU = 13
    DOT_COULOIR_ANGLE = 14
    DOT_COULOIR_STOCKAGE = 15
    DOT_OPENSPACE = 16
    DOT_NOWHERE = 17
dots = NFC_Dot()

#LOC
ROOM_NFC_MATCH = np.array([ [   rooms.NOWHERE,       rooms.STAGIAIRE,         rooms.MANAGER,        rooms.PAUSE,          rooms.REUNION,        rooms.ENTREE,         rooms.BUREAU,         rooms.OPENSPACE        ], 
                            [   dots.DOT_NOWHERE,    dots.DOT_STAGIAIRE,      dots.DOT_MANAGER,     dots.DOT_PAUSE,       dots.DOT_REUNION,     dots.DOT_ENTREE,      dots.DOT_BUREAU,      dots.DOT_OPENSPACE     ]])
#Loc Home
DOT_POSITION_TO_X_MATCH = np.array([[TL.NFC_LOC_0_0[0]],
                                    [TL.NFC_LOC_1_0[0]],
                                    [TL.NFC_LOC_2_0[0]],
                                    [TL.NFC_LOC_3_0[0]],
                                    [TL.NFC_LOC_4_0[0]],
                                    [TL.NFC_LOC_5_0[0]],
                                    [TL.NFC_LOC_6_0[0]],
                                    [TL.NFC_LOC_7_0[0]],
                                    [TL.NFC_LOC_8_0[0]],
                                    [TL.NFC_LOC_9_0[0]],
                                    [TL.NFC_LOC_10_0[0]],
                                    [TL.NFC_LOC_11_0[0]],
                                    [TL.NFC_LOC_12_0[0]],
                                    [TL.NFC_LOC_13_0[0]],
                                    [TL.NFC_LOC_14_0[0]],
                                    [TL.NFC_LOC_15_0[0]],
                                    [TL.NFC_LOC_16_0[0]]])

DOT_POSITION_TO_Y_MATCH = np.array([[TL.NFC_LOC_0_0[1]],
                                    [TL.NFC_LOC_1_0[1]],
                                    [TL.NFC_LOC_2_0[1]],
                                    [TL.NFC_LOC_3_0[1]],
                                    [TL.NFC_LOC_4_0[1]],
                                    [TL.NFC_LOC_5_0[1]],
                                    [TL.NFC_LOC_6_0[1]],
                                    [TL.NFC_LOC_7_0[1]],
                                    [TL.NFC_LOC_8_0[1]],
                                    [TL.NFC_LOC_9_0[1]],
                                    [TL.NFC_LOC_10_0[1]],
                                    [TL.NFC_LOC_11_0[1]],
                                    [TL.NFC_LOC_12_0[1]],
                                    [TL.NFC_LOC_13_0[1]],
                                    [TL.NFC_LOC_14_0[1]],
                                    [TL.NFC_LOC_15_0[1]],
                                    [TL.NFC_LOC_16_0[1]]])
