/* I2C master code...*/
/* This is the code of the main Arduino
    It control the motor and the oven under
    user serial instructions... 
*/
#include "my_max6675.h"
#include <PID_v1.h>
#include <Wire.h> // for I2C comunication S

//code based on https://electronoobs.com/eng_arduino_tut24.php

int PWM_pin = 11; // PID output pin
double Setpoint;   // temperature setpoint.

double temperature = 0; // PID input
double PID_output = 0; // PID output

long int rpm_speed = 400;
int position = 0;

bool oven_state = false;

//PID tunnnig parameters
//////////////////////////////////////////////////////////
double kp =2;  double ki = 5;  double kd = 1;
//////////////////////////////////////////////////////////

PID PID_controller(&temperature, &PID_output, &Setpoint, kp, ki, kd, DIRECT);

//pin declaration

int PID_CS_PIN = 2;
int T1_CS_PIN = 3;
int T2_CS_PIN = 4;
int T3_CS_PIN = 5;
int T4_CS_PIN = 6;
int T5_CS_PIN = 7;

MY_MAX6675 PID_sensor(PID_CS_PIN);
MY_MAX6675 T1_sensor(T1_CS_PIN);
MY_MAX6675 T2_sensor(T2_CS_PIN);
MY_MAX6675 T3_sensor(T3_CS_PIN);
MY_MAX6675 T4_sensor(T4_CS_PIN);
MY_MAX6675 T5_sensor(T5_CS_PIN);

void setup(){
    //Serial.begin(9600);
    Serial.begin(115200);
    pinMode(PWM_pin, OUTPUT);
    Wire.begin();

    // intialize variables
    temperature = PID_sensor.readCelsius();
    Setpoint = 50;

    // turn the PID on
    PID_controller.SetMode(AUTOMATIC);
    PID_controller.SetSampleTime(250);

}

void loop(){
    if( oven_state){
        // Read the current value of temperature
        temperature = PID_sensor.readCelsius();
        PID_controller.Compute();

        analogWrite(PWM_pin, 255-PID_output); // PID_output lives in [0, 255]
    }
    else{
        analogWrite(PWM_pin, 255); // off
    }

    delay(250); // wait because the thermocouple resolution
}

void serialEvent(){
    String command  = Serial.readString();
    //measure commands
    if (command[0] == 'g'){ // g --> get data
        Serial.print("{\"T1\":");
        Serial.print(T1_sensor.readCelsius());
        Serial.print(",");  
        Serial.print("\"T2\":");
        Serial.print(T2_sensor.readCelsius());
        Serial.print(",");        
        Serial.print("\"T3\":");
        Serial.print(T3_sensor.readCelsius());
        Serial.print(",");
        Serial.print("\"T4\":");
        Serial.print(T4_sensor.readCelsius());
        Serial.print(",");        
        Serial.print("\"T5\":");
        Serial.print(T5_sensor.readCelsius());
        Serial.print(",");
        Serial.print("\"T_PID\":");
        Serial.print(temperature);
        Serial.println("}");
    }

    // ---------------------- oven commands --------------------
    if (command.substring(0, 2) == "eo"){ // eo --> enable oven
        oven_state = true;
        Serial.println("Oven Enabled");
    }

    if (command.substring(0, 2) == "do"){ // do --> enable oven
        oven_state = false;
        Serial.println("Oven Disabled");
    }
    if (command[0] == 's'){
        Setpoint = command.substring(1).toInt();
        Serial.println("SetPoint: " + command.substring(1));
    }
    if (command[0] == 'k'){
        if (command[1] == 'p')
            kp = command.substring(2).toInt();
        if (command[1] == 'i')
            ki = command.substring(2).toInt();
        if (command[1] == 'd')
            kd = command.substring(2).toInt();

        PID_controller.SetTunings(kd, ki, kd);
        Serial.println("Tunnnig parameters chaged");
    }
    // --------------------- motor commands --------------------
    if (command[0] == 'v'){ // v --> speed
        rpm_speed = command.substring(1).toInt();
        setSpeed();
        Serial.println("Speed was set to " + command.substring(1));
    }
    if (command.substring(0, 2) == "em"){ // em --> Enable
        enable();
        Serial.println("Motor Enable");
    }
    if (command.substring(0, 2) == "dm"){ // dm --> disable
        disable();
        Serial.println("Moto disable");
    }
    if (command[0] == 'p'){ // p --> set new Position
        position = command.substring(1).toInt();
        setPosition();
        Serial.println("new Position: " + command.substring(1));
    }
    if (command[0] == 'c'){ // c --> set cero position
        zeroRef();
        Serial.println("New 0-ref");
    }
}
void setSpeed(){
    Wire.beginTransmission(0X01);
    Wire.write('v');
    String aux_rpm = String(rpm_speed);
    // it is necessary to send character by character
    for(int i =0; i < aux_rpm.length(); i++ ) {
        Wire.write(aux_rpm[i]);
    }
    Wire.endTransmission();
}
void enable(){

    Wire.beginTransmission(0X01);
    Wire.write('e');
    Wire.endTransmission();
}
void disable(){;
    Wire.beginTransmission(0X01);
    Wire.write('d');
    Wire.endTransmission();
}

void setPosition(){
    Wire.beginTransmission(0X01);
    Wire.write('p');
    String aux_pos = String(position);
    // it is necessary to send character by character
    for(int i =0; i < aux_pos.length(); i++ ) {
        Wire.write(aux_pos[i]);
    } 
    Wire.endTransmission();
}

void zeroRef(){
    Wire.beginTransmission(0X01);
    Wire.write('c');
        Wire.endTransmission();
}
