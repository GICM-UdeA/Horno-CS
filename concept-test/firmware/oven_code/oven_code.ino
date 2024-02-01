#include "thermocouple.h"
#include <PID_v1.h>

//code based on https://electronoobs.com/eng_arduino_tut24.php

int PWM_pin = 9; // PID output pin
double Setpoint;   // temperature setpoint.

double temperature = 0; // PID input
double PID_output = 0; // PID output
int button_pressed = 0;
int menu_activated=0;

//PID tunnnig parameters
//////////////////////////////////////////////////////////
double kp =2;  double ki = 5;  double kd = 1;
//////////////////////////////////////////////////////////

PID PID_controller(&temperature, &PID_output, &Setpoint, kp, ki, kd, DIRECT);

void setup()
{
    Serial.begin(9600);
    pinMode(PWM_pin, OUTPUT);
    set_thermocouple(4, 5, 6);
    
    // intialize variables
    temperature = measure_temp();
    Setpoint = 50;

    // turn the PID on
    PID_controller.SetMode(AUTOMATIC);
    PID_controller.SetSampleTime(250);

}

void loop()
{
    // Read the current value of temperature
    temperature = measure_temp();
    PID_controller.Compute();

    analogWrite(PWM_pin, 255-PID_output); // PID_output lives in [0, 255]

    Serial.println(temperature);

    delay(250); // wait because the thermocouple resolution
}

void serialEvent(){
    String command  = Serial.readString();

    if (command[0] == 'S'){
        Setpoint = command.substring(1).toInt();
    }
    if (command[0] == 'k'){
        if (command[1] == 'p')
            kp = command.substring(2).toInt();
        if (command[1] == 'i')
            ki = command.substring(2).toInt();
        if (command[1] == 'd')
            kd = command.substring(2).toInt();

        PID_controller.SetTunings(kd, ki, kd);
    }
}
