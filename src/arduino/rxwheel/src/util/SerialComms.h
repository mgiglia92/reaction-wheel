#include <string.h>
#include <Arduino.h>
#include "util/pid-control.h"
#include "util/structures.h"

class SerialComms{
public:
    //Process a command received from serial buffer
    void processCommand(char*);
    //Search cmd for letter, return number immideately after letter
    long parseNumberInt(char*, char, int);
    double parseNumberDouble(char*, char, int);
    //Get controller values from string 
    void getControllerVals(char*, PID_control_config_t*);
    // SerialComms(int*, double*, pwmAngle, pwmVelocity, time);
    SerialComms();

    void handleCommand();
    void sendData(double, double, double, double, double);

    //-------
    //Serial communication buffer params
    char cmd [200]; //Input command from serial
    int cmd_index; //Current index in cmd[] 
    char incoming_char; //Serial incoming character for "parallel processing" of serial data


    //--------------------------
    //Local variables to hold data from serial stream
    int labType;
    double setpoint;
    int mode;
    bool startTest;
    bool runController;
    bool activate; // Activate/deactivate controllers and comms
    PID_control_config_t config0;
    PID_control_config_t config1;
    PID_control_config_t config2;
    PID_control_config_t config3;
    PID_control_config_t config4;
    CmdVals_t cmdVals;
    bool calibration_start;
    int anti_windup_activated;
    int LPF;
    bool writeData;
    bool updateParams; //Flag to update values outside this class
    bool updateController;
};


/*
"""
From Arduino:
Z0,A#,B#,C#,D# # Data from the Arduinos sensors or actuator commands

To Arduino:

IMPORTANT:
Reserved Initial Characters: E,R,T,S,M,K,

Serial Comms "G-code" style lookup:

E0 : SOFTWARE E-STOP

R0 : Deactivate controllers and comms
R1 : Activate test and comms (deactivate controller)
R2 : Activate controller and comms (deactivate test)

Make sure YAML file controller types are same as firmware expected controller types
(0: PID, 1: cascade, 2: PID w/ feedforward)
T0,A#(int),B#(int),C#(int),D#(int),E#(int),F#(int) : Confirm the controller types

//Set signals
S0,A#(float) : Set angle set point
S1,A#(float) : Set angular vel set point

//Set Modes
M0,A#(float) : step input test
M1,A#(int) : Set IMU Parameters lowpass filter settings


Set Gains: PID gains and Feed forward gains (F)
P: proportiona, I: Integral, D: derivative, F: feedforward, T: sample time, B: Derivative cutoff freq
L: Lower output limit, U: upper output limit, E: deadband radius
All # are doubles here!
K0,P#,I#,D#,F#,T#,B#,L#,U#,E# : Set Gains of Controller0
K1,P#,I#,D#,F# : Set Gains of Controller1
K2,P#,I#,D#,F# : Set Gains of Controller2
K3,P#,I#,D#,F# : Set Gains of Controller3
K4,P#,I#,D#,F# : Set Gains of Controller4
K5,P#,I#,D#,F# : Set Gains of Controller5
K6,P#,I#,D#,F# : Set Gains of Controller6
K7,P#,I#,D#,F# : Set Gains of Controller7
K8,P#,I#,D#,F# : Set Gains of Controller8
K9,P#,I#,D#,F# : Set Gains of Controller9


"""
*/

// S0,P0.1,I0,D0,%
// S1,Z100,%
// S2,Y0,%
// S3,M1,%
// S4,T0.005,%
// S5,L-12,U12,%