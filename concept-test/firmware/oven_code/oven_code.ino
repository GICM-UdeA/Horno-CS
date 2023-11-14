#include "thermocouple.h"

//code based on https://electronoobs.com/eng_arduino_tut24.php

int PWM_pin = 9;

float goal_temperature = 50;   //Default temperature setpoint.

float temperature = 0;
float PID_error = 0;
float previous_error = 0;
float elapsedTime, Time, prev_time;
float PID_value = 0;
int button_pressed = 0;
int menu_activated=0;
float last_goal_temperature = 0;

//PID constants
//////////////////////////////////////////////////////////
int kp =20;   int ki = 40;   int kd = 0;
//////////////////////////////////////////////////////////

int PID_p = 0;    int PID_i = 0;    int PID_d = 0;

void setup()
{
    Serial.begin(9600);
    pinMode(PWM_pin, OUTPUT);
    set_thermocouple(4, 5, 6);
    Serial.begin(9600);
    Time = millis();

}

void loop()
{
    // Read the real value of temperature
    temperature = measure_temp();
    //Serial.print("temperature = ");
    Serial.println(temperature);
//    Serial.print("\t PID = ");
//    Serial.println(PID_value);
    
    //Next we calculate the error between the setpoint and the real value
    PID_error = goal_temperature - temperature + 3;

    //Calculate the P value
    PID_p = 0.01 * kp * PID_error;

    //Calculate the I value in a range on +-3
    PID_i = 0.01 * PID_i + (ki * PID_error);
    

    //For derivative we need real time to calculate speed change rate
    prev_time = Time;
    Time = millis();
    elapsedTime = (Time - prev_time) / 1000; 

    //Calculate the D value
    PID_d = 0.01 * kd * ((PID_error - previous_error) / elapsedTime);
    //Final total PID value is the sum of P + I + D
    PID_value = PID_p + PID_i + PID_d;
    
    PID_value = constrain(PID_value, 0, 255);

    analogWrite(PWM_pin, 255-PID_value);
    previous_error = PID_error;     //Store the error for next loop.

    delay(250);
}

void serialEvent(){
    double value = Serial.parseFloat();
    goal_temperature = constrain(value, 0, 200);
    Serial.print("goal temp set to ");
    Serial.println(goal_temperature);
}
