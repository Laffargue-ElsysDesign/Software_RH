from signal import signal, SIGINT
from pynq import Overlay
#import lib.rfid_driver
from time import sleep

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. HOLOCOM Exiting gracefully')
    exit(0) 

class RFID():
    def __init__(self, overlay):
        self.rfid = overlay.RFID_reader_0

    def Check_RFID(self):
        New = self.rfid.Read_Tag_Detect()
        return New
    
    def Read_Data(self):
        while not (self.rfid.Read_Tag_Data_Valid):
            pass
        point, position = self.rfid.Read_Tag()
        self.rfid.Reset()
        return (point, position)

if __name__ == '__main__':
    signal(SIGINT, handler)
    
    global overlay
    overlay = Overlay("../Overlays/US2/BitStream/bitstream.bit")
    overlay.download()
    rfid = RFID(overlay)
    while(1):
        if rfid.Check_RFID():
            print("RFID_Detected ", rfid.Read_Data())
        else:
            print("Nothing detected")
        sleep(0.5)