#include "thermocouple.h"

float goal_temperature = 50;   //Default temperature setpoint.

float temperature = 0;
float PID_error = 0;
int PID_p = 0;

int PWM_pin = 9;
int PWM_value = 50;

//PID constant
////////////
int kp =300; 
///////////

void setup() {
  Serial.begin(9600);
  pinMode(PWM_pin, OUTPUT);
  set_thermocouple(4, 5, 6);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  temperature = measure_temp();
  //Serial.print("temperature=");
  Serial.println(temperature);
//  Serial.print(";\t PID = ");
//  Serial.print(PID_p);
//  Serial.print(";\t PWM = ");
//  Serial.println(PWM_value);

  //Next we calculate the error between the setpoint and the real value
  PID_error = goal_temperature - temperature;

  //Calculate the P value
  PID_p = 0.01 * kp * PID_error;

  PWM_value = constrain(PWM_value + PID_p,0, 255);

  analogWrite(PWM_pin, 255 - PWM_value);

  delay(250);
}

void serialEvent(){
  double value = Serial.parseFloat();
  goal_temperature = constrain(value, 0, 200);
  Serial.print("goal temp set to ");
  Serial.println(goal_temperature);
}
