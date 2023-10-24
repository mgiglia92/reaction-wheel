#include "SerialComms.h"


SerialComms::SerialComms(){
    //Initialize Serial buffer params
    cmd_index=0;
    writeData=false;

    //Variable that get used externally, set via the command protocol
    setpoint = 0;
    mode = 0;
    cmdVals.startTest=false;
    cmdVals.runController=false;
    activate = false;
    calibration_start = false;
    LPF=0;

    updateParams = false;
}

void SerialComms::processCommand(char* cmd_string){
    int pos;
    int cmd;

    //E-STOP
    cmd = parseNumberInt(cmd_string, 'E', -1);
    switch((int)(cmd)){
        case 0:
            break;
        default: break;
    }

    //TODO: Add R3, send data, no controls, no test
    //Request start stop
    cmd = parseNumberInt(cmd_string, 'R', -1);
    switch((int)(cmd)){
        case 0: //Deactivate control and comms
            cmdVals.startTest = false;
            cmdVals.runController = false;
            writeData=false;
            updateParams = true;
            break;
        case 1: //Activate test
            cmdVals.startTest = false;
            //TODO: Undo this, edit for showcase
            // cmdVals.startTest = true;
            cmdVals.runController = false;
            writeData=true;
            updateParams = true;
            break;
        case 2: //Activate feedback control
            cmdVals.runController = true;
            cmdVals.startTest = false;
            writeData =true;
            updateParams = true;
            break;

        //If no matches, break
        default: break;
    }

    //Set value/mode commands
    cmd = parseNumberInt(cmd_string, 'S', -1);
    switch(int(cmd)){
        case 0: //Set angle set point
            cmdVals.thetaSetpoint = parseNumberDouble(cmd_string, 'A', 0);
            updateParams = true;
            break;

        case 1://Set ang vel set point
            cmdVals.thetaDotSetpoint = parseNumberDouble(cmd_string, 'A', 0);
            updateParams = true;
            break;

        default: break;
    }

    //Set controller gains and other parameters
    cmd = parseNumberInt(cmd_string, 'K', -1);
    switch((int)(cmd)){
        double p;
        double i;
        double d;
        double f;
        double t;
        double b;
        double l;
        double u;
        double e;

        case 0:
            getControllerVals(cmd_string, &config0);
            updateController=true;
            break;
        case 1:
            getControllerVals(cmd_string, &config1);
            updateController=true;
            break;
        case 2:
            getControllerVals(cmd_string, &config2);
            updateController=true;
            break;
        case 3:
            getControllerVals(cmd_string, &config3);
            updateController=true;
            break;
        case 4:
            getControllerVals(cmd_string, &config4);
            updateController=true;
            break;
        default: break;
    }

    //Set Modes
    cmd = parseNumberInt(cmd_string, 'M', -1);
    switch((int)(cmd)){
        case 0: //Step input test mode
        
            break;
        case 1: //Set IMU accel and gyro lowpass filter settings
            LPF = constrain(parseNumberInt(cmd_string, 'A', 0),0,6);
            updateParams = true;
            break;
        default: break;
    }
}

long SerialComms::parseNumberInt(char* cmd_string, char key, int def){
    //Search cmd_string for key, return the number between key and delimiter
    // Serial.println(cmd_string);
    // Serial.println(key);

    int key_len=0; //Position of key in string
    int delim_len=0; //Position of next delimiter after key in string

    //Search string for first instance of key, increment key length each time key isn't found
    for(int i=0; i<100; i++) //TODO: Make this 100 value a HEADER_LENGTH #define
    {
        if(cmd_string[i] == '\0') { return def; } //If we can't find key, return default value
        if(cmd_string[i] == key){key_len = i; break;}
    }
    // Serial.print("key len: "); Serial.println(key_len);

    //Search string starting at character after key, looking for next delimiter the comma
    for(int i=key_len+1; i<100; i++){
        if(cmd_string[i] == ',' || cmd_string[i] == '\0')
        {
            break;
        }
        delim_len++;
    }
    // Serial.print("delim len: "); Serial.println(delim_len);

    //Create empty substring to use strncpy
    char substring[20] = {0};
    strncpy(substring, &cmd_string[key_len+1], delim_len);  //Copy subset of string to substring
    
    // Serial.print("test string: "); Serial.println(substring);
    return atoi(substring); //return the substring in int format
}

double SerialComms::parseNumberDouble(char* cmd_string, char key, int def){
    //Search cmd_string for key, return the number between key and delimiter
    // Serial.println(cmd_string);
    // Serial.println(key);

    int key_len=0; //Position of key in string
    int delim_len=0; //Position of next delimiter after key in string

    //Search string for first instance of key, increment key length each time key isn't found
    for(int i=0; i<100; i++) //TODO: Make this 100 value a HEADER_LENGTH #define
    {
        if(cmd_string[i] == '\0') { return def; } //If we can't find key, return default value
        if(cmd_string[i] == key){key_len = i; break;}
    }
    // Serial.print("key len: "); Serial.println(key_len);

    //Search string starting at character after key, looking for next delimiter the comma
    for(int i=key_len+1; i<100; i++){
        if(cmd_string[i] == ',' || cmd_string[i] == '\0')
        {
            break;
        }
        delim_len++;
    }
    // Serial.print("delim len: "); Serial.println(delim_len);

    //Create empty substring to use strncpy
    char substring[20] = {0};
    strncpy(substring, &cmd_string[key_len+1], delim_len);  //Copy subset of string to substring
    
    // Serial.print("test string: "); Serial.println(substring);
    return atof(substring); //return the substring in float format
}

void SerialComms::handleCommand(){
// Arduino command handler
  if (Serial.available() != 0) {
    incoming_char = Serial.read();
    cmd[cmd_index] = incoming_char;
    if (incoming_char == '\0' || incoming_char == '%') {
      //      Serial.println("End of line, processing commands!");
      processCommand(cmd);
      // Reset comparse_number and buffer
      cmd_index = 0;
      memset(cmd, '\0', sizeof(cmd));
    }
    else {
      cmd_index ++;
    }
  }
}

void SerialComms::sendData(double a, double b, double c, double d, double e) {

    if(writeData)
    {
        Serial.print('$'); //Start of message char
        Serial.print('Z'); Serial.print(0); Serial.print(',');
        Serial.print('A'); Serial.print(a,6); Serial.print(',');
        Serial.print('B'); Serial.print(b,2); Serial.print(',');
        Serial.print('C'); Serial.print(c,2); Serial.print(',');
        Serial.print('D'); Serial.print(d,2); Serial.print(',');
        Serial.print('E'); Serial.print(e,2);
        Serial.print('%'); //End of message character
        // Serial.println('\0');
    }
}

void SerialComms::getControllerVals(char* cmd_string, PID_control_config_t* config)
{       
    double p = parseNumberDouble(cmd_string, 'P', 0);
    double i = parseNumberDouble(cmd_string, 'I', 0);
    double d = parseNumberDouble(cmd_string, 'D', 0);
    double f = parseNumberDouble(cmd_string, 'F', 0);
    double t = parseNumberDouble(cmd_string, 'T', 0.01);
    double b = parseNumberDouble(cmd_string, 'B', 0.1);
    double l = parseNumberDouble(cmd_string, 'L', 0);
    double u = parseNumberDouble(cmd_string, 'U', 0);
    double e = parseNumberDouble(cmd_string, 'E', 0);
    config->kp = p;
    config->ki = i;
    config->kd = d;
    config->ts = t;
    config->sigma = b;
    config->lowerLimit = l;
    config->upperLimit = u;

}