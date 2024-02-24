/*Motor code...*/
#include <Wire.h> //S

#include "AccelStepper.h"
#define motorInterfaceType 1

// pins definition
int enb_pin = 7;
int dir_pin = 8;
int step_pin = 9;

// auxiliary variables
bool start_round;
long int rpm_speed = 400;
long int newPosition = 0;
int dir = 1; // counterclockwise by default

AccelStepper stepper(motorInterfaceType, step_pin, dir_pin);

void setup(){
    Wire.begin(0x01); // I2C address: 1 S
    Serial.begin(115200);
    // pins configuration
    pinMode(enb_pin, OUTPUT);

    pinMode(LED_BUILTIN, OUTPUT);

  // interruptions defined by end of the rounds
    stepper.setCurrentPosition(0);
    stepper.setMaxSpeed(1000);

    Wire.onReceive(controllerI2C); //S
}

void loop(){

    if (start_round){
        if(abs(stepper.currentPosition() - newPosition) > 0){
            stepper.setSpeed(rpm_speed);
            stepper.runSpeed();
            Serial.println("pos:" + String(stepper.currentPosition()));
        }
    }
}

void serialEvent(){
  // receiving command
    String command = Serial.readString();
    processCommand(command);
}

void controllerI2C(){ // S
    // receiving command
    String command = "";

    while(Wire.available()){
    char c = Wire.read();
    command += String(c);
    processCommand(command);
    }
}

void processCommand(String command){
    if (command[0] == 'v'){ // v --> speed
        rpm_speed = command.substring(1).toInt();
        Serial.println("Speed was set to " + command.substring(1));
    } 
    if (command[0] == 'e'){ // e --> Enable
        start_round = true;
        digitalWrite(enb_pin, 0);
        digitalWrite(LED_BUILTIN, 1); // led running indicator
        Serial.println("Enable");
    }  
    if (command[0] == 'd'){ // d --> disable
        start_round = false;
        digitalWrite(enb_pin, 1);
        digitalWrite(LED_BUILTIN, 0); // led running indicator
        Serial.println("Disable");
    }

    if (command[0] == 'p'){ // p --> set new Position
        newPosition = command.substring(1).toInt();

        if (newPosition - stepper.currentPosition() > 0)
            if (dir == 0)
                goForward();
        if (newPosition - stepper.currentPosition() < 0)
            if (dir == 1)
                goBackward();

        Serial.println("new Position: " + command.substring(1));
    }
    if (command[0] == 'c'){ // c --> set cero position
        stepper.setCurrentPosition(0);
        Serial.println("New 0-ref");
    }
}

void goForward(){
    if (rpm_speed < 0)
        rpm_speed = -1 * rpm_speed;
    dir = 1;
}

void goBackward(){
    if (rpm_speed > 0)
        rpm_speed = -1 * rpm_speed;
    dir = 0;
}