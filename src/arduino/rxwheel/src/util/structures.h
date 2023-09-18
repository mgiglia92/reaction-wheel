#ifndef RXWHEEL_STRUCTURES_H
#define RXWHEEL_STRUCTURES_H

typedef struct CmdVals_s{
    float thetaSetpoint;
    float thetaDotSetpoint;
    int controlType; //Theta control, or thetaDot control
    bool startTest;
    bool runController;
} CmdVals_t;

#endif