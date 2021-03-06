from pynq import DefaultIP
import time

ADDRESS_UARTLITE = 0x0042C00000
CTRL_REG = 0x0C
RST_REG = 0x03
RX_FIFO = 0x00
STATUS_REG = 0x08
TX_FIFO = 0x04

class UARTDriver(DefaultIP):
    def __init__(self, description):
        super().__init__(description=description)
        self.reset()
    bindto = ['xilinx.com:ip:axi_uartlite:2.0']
    
    def reset(self):
        self.write(CTRL_REG,RST_REG)
        time.sleep(0.1)
        self.write(CTRL_REG,RX_FIFO)
    
    def writeByte(self, buf, timeout = 2):
        """Send a message
        Return number of bytes succesfully sent
        buf: iterable

        """
        
        wr_count = 0
        for i in buf:
            stop_time = time.time() + timeout
            #Wait while TX FIFO is Full, stop waiting if timeout passes 
            while ((self.read(STATUS_REG)>>3) & 1) and (time.time()<stop_time):
                pass
            if time.time()>stop_time:
                raise ValueError("Send timeout")
            
            self.write(TX_FIFO, (i))
            wr_count += 1
            
        while ((self.read(STATUS_REG)>>2) & 1)==0:
                pass
        return wr_count 
    
    
    def readByte(self,timeout=2):
        """Read a single byte
        Return -1 in case of timeout
        Return value sucessfully read
        
        """
        stop_time = time.time() + timeout
        while (self.read(STATUS_REG) & 1)==0 and (time.time()<stop_time):
            pass
        if time.time()>stop_time:
            raise ValueError("Read timeout")
        return self.read(RX_FIFO)
    
    def readNBytes(self, n, timeout=10):
        """Read n bytes
        Return -1 in case of timeout
        Return iterable of read bytes
        
        """
        buf=[]
        for i in range(n):
            read_byte=self.readByte(timeout)
            buf.append(read_byte)
        
        return buf 
        
    def readMessage(self, SOF, EOF, msg_len, max_iter, timeout=10):
        """Read bytes until stop_value is read.
        Return -1 in case of timeout
        Return iterable of read bytes
        
        """
        buf=[0]*msg_len
        read_byte=self.readByte(timeout)
        buf.append(read_byte)
        #print("sof=",SOF)
        i=0
        buf.pop(0)
        message_received=False
        
        while not(message_received):
            read_byte=self.readByte(timeout)
            buf.append(read_byte)
            buf.pop(0)
            #print(buf)
            if (buf[-1]==EOF and buf[0]==SOF):
                message_received=True
            if i>max_iter :
                #print(buf)
                raise ValueError("Max buf length")
            i=i+1
        
        return buf 
        
