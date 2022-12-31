from threading import Thread
from queue import Queue
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial
from util.data_util import DataFormat

BOM = '$' # Beginning of message character
EOM = '%' # End of message character
CS = "&&&***" # Test Completed message

class ArduinoComms(Serial):
    def __init__(self, port=None, baudrate=115200, \
                bytesize=EIGHTBITS, parity=PARITY_NONE, \
                stopbits=STOPBITS_ONE, timeout=10):

        super(Serial, self).__init__(port=port, baudrate=baudrate, bytesize=bytesize, \
                                parity=parity, stopbits=stopbits, timeout=timeout)
        
        self.dataQueue = Queue(maxsize=1000) # Queue of Data from arduino
        self.outQueue = Queue(maxsize=100) # Queue of messages waiting for response
        self.outputBufferQueue = Queue(maxsize=100) # Queueof output messages to arduino
        self.responseQueue = Queue(maxsize=100) # Queue of responses from arduino based on output messages
        self.commsProcess = Thread(target=self.startComms)
        self.messageBuffer = Queue(maxsize=1000)
        self.data = DataFormat()

    def connect(self, port=None):
        try:
            self.port = port
            self.open()
            if(self.isOpen()): print("Succesfully Connected!")
            self.set_buffer_size(rx_size = 12800, tx_size = 12800)
            self.flush()
            self.commsProcess.start()
        except Exception as e:
            print(e)
            print(f"or maybe {self.port}, is not valid")
    
    def startComms(self):
        while True:
            try:
                pass
                # Check if any any messages in output queue
                if not self.outputBufferQueue.empty():
                    self.write(bytes(self.outputBufferQueue.get(), 'utf-8'))
                # Check if any data available 
                if self.in_waiting > 0:
                    msg = self.read_until(bytes(EOM, 'utf-8'))
                    msg = msg.decode('utf-8')
                    if self.checkValidMessage(msg):
                        self.decipherMessage(msg)
                    else:
                        print("invalid message")
            except:
                pass
    
    def decipherMessage(self, msg: str):
        # Remove BOM and EOM
        stripped = msg[1:-1]
        # Split message by commas
        sub = stripped.split(',')
        # Check if the first command is 'Z0' if so it's data
        if(sub[0] == "Z0"):
            # append to dataqueue
            self.dataQueue.put(sub[1:])
        
        return sub[1:]

    def sendMessage(self, msg: str):
        if(self.checkValidMessage(msg)):
            self.outputBufferQueue.put(msg)
    
    def checkOutputQueue(self):
        pass

    def ESTOP(self):
        pass

    def checkValidMessage(self, msg:str):
        if(msg[0] is not BOM): return False
        elif(msg[-1] is not EOM): return False
        else: return True
    
    # This needs to be more modular, for now just parses the 
    # passed in data and returns as tuple
    def processDataMessage(self, data):
        time = data[0][1:]
        ax = data[1][1:]
        az = data[2][1:]
        wy = data[3][1:]
        power = data[4][1:]
        return (float(time), float(ax), float(az), float(wy), float(power))

"""
From Arduino:
Z0,A#,B#,C#,D# # Data from the Arduinos sensors or actuator commands

To Arduino:

Serial Comms "G-code" style lookup:

E0 : SOFTWARE E-STOP

S0 : Stop
S1 : Start

Make sure YAML file controller types are same as firmware expected controller types
(0: PID, 1: cascade, 2: PID w/ feedforward)
K0,A#(int),B#(int),C#(int),D#(int),E#(int),F#(int) : Confirm the controller types

Set Gains: PID gains and Feed forward gains (F)
All # are doubles here!
C0,P#,I#,D#,F# : Set Gains of Controller0
C1,P#,I#,D#,F# : Set Gains of Controller1
C2,P#,I#,D#,F# : Set Gains of Controller2
C3,P#,I#,D#,F# : Set Gains of Controller3
C4,P#,I#,D#,F# : Set Gains of Controller4
C5,P#,I#,D#,F# : Set Gains of Controller5
C6,P#,I#,D#,F# : Set Gains of Controller6
C7,P#,I#,D#,F# : Set Gains of Controller7
C8,P#,I#,D#,F# : Set Gains of Controller8
C9,P#,I#,D#,F# : Set Gains of Controller9

Set IMU Parameters # without (type) are double.
I0,A#(int),G#(int) : Set Accel Low pass setting and Gyro Low pass setting

"""

if __name__ == "__main__":
    from util.data_util import DataFormat
    d = DataFormat()
    a = ArduinoComms()
    a.connect(port="COM14")
    while True:
        d.append(a.processDataMessage(a.dataQueue.get()))
        print(d.time.shape)