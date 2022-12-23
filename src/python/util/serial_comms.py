from multiprocessing import Process, Queue, SimpleQueue
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

class ArduinoComms(Serial):
    def __init__(self, port=None, baudrate=115200, \
                bytesize=EIGHTBITS, parity=PARITY_NONE, \
                stopbits=STOPBITS_ONE, timeout=10):

        super(Serial, self).__init__(port=port, baudrate=baudrate, bytesize=bytesize, \
                                parity=parity, stopbits=stopbits, timeout=timeout)

    def connect(self, port=None):
        try:
            self.port = port
            self.open()
            if(self.isOpen()): print("Succesfully Connected!")
        except Exception as e:
            print(e)
            print(f"Maybe {self.port}, is not valid")


"""
Serial Comms "G-code" style lookup:

E0 : SOFTWARE E-STOP

S0 : Stop
S1 : Start

C0,P#,I#,D#,F# : Set Gains of Controller0
C1,P#,I#,D# : Set Gains of Controller1
C2,P#,I#,D# : Set Gains of Controller2
C3,P#,I#,D# : Set Gains of Controller3
C4,P#,I#,D# : Set Gains of Controller4
C5,P#,I#,D# : Set Gains of Controller5
C6,P#,I#,D# : Set Gains of Controller6
C7,P#,I#,D# : Set Gains of Controller7
C8,P#,I#,D# : Set Gains of Controller8
C9,P#,I#,D# : Set Gains of Controller9


"""
"""
Serial Comms "G-code" style lookup:

E0 : SOFTWARE E-STOP

S0 : Stop
S1 : Start

Set Gains: PID gains and Feed forward gain (F)
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