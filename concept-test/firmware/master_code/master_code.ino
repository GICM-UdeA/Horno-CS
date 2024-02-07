/* I2C master code...*/
/* This is the code of the main Arduino
  It control the motor and the oven under
  user serial instructions... 
*/

#include "max6675.h" 
#include <PID_v1.h>
#include <Wire.h> // for I2C comunication

// PID Thermocouple pins
const int MAX6675_SO_PID = 4;
const int MAX6675_CS_PID = 5;
const int MAX6675_SCK_PID = 6;

// monitoring Thermocouple pins
const int MAX6675_SO = 7;
const int MAX6675_CS = 8;
const int MAX6675_SCK = 9;

// setting up thermocouples
MAX6675 PID_input_sensor(MAX6675_SCK_PID, MAX6675_CS_PID, MAX6675_SO_PID);
MAX6675 temp_sensor(MAX6675_SCK, MAX6675_CS, MAX6675_SO);

// to enable the measurement
volatile bool measure_temp = false;

// to stop the measurement
const int end_pin = 3;

// speed variable
int rpm_value = 0;

int PWM_pin = 11; // PID output pin
double Setpoint;   // temperature setpoint.

double temperature = 0; // PID input
double PID_output = 0; // PID output

//PID tunnnig parameters
//////////////////////////////////////////////////////////
double kp =2;  double ki = 5;  double kd = 1;
//////////////////////////////////////////////////////////

PID PID_controller(&temperature, &PID_output, &Setpoint, kp, ki, kd, DIRECT);

void setup() {

  pinMode(end_pin, INPUT);
  Serial.begin(115200);
  Wire.begin();

  // intialize variables
  temperature = PID_input_sensor.readCelsius();
  Setpoint = 50;

  // turn the PID on
  PID_controller.SetMode(AUTOMATIC);
  PID_controller.SetSampleTime(250);

  attachInterrupt(digitalPinToInterrupt(end_pin), end_measure, FALLING);
}

void loop() {
  if (measure_temp){
    temperature = PID_input_sensor.readCelsius();
    PID_controller.Compute();

    analogWrite(PWM_pin, 255-PID_output); // PID_output lives in [0, 255]

    Serial.print("T_PID:");
    Serial.print(temperature);
    Serial.print(",");
    Serial.print("T:");
    Serial.println(temp_sensor.readCelsius());

    delay(250);
  }
}

void serialEvent() {
  /*Command codification*/
  
  String command = Serial.readString();
  
  if (command[0] == 'V'){ // S --> to set the speed (in rpm)
    rpm_value = command.substring(1).toInt();
    set_rpm();
  } 
  if (command[0] == 'R'){ // R --> to start the measurement
    run_measurement();
  }
  if (command[0] == 'r'){ // r --> to stop and reset the parameters of the motor
    reset_motor();
  }
  if (command[0] == 'i'){ // i --> to invert the movement direction
    invert_motor();
  }
  if (command[0] == 's'){ // s --> to stablish the setPoint temperature
        Setpoint = command.substring(1).toInt();
    }
    if (command[0] == 'k'){ // k+{p, i, d} --> to stablish the PID constants
        if (command[1] == 'p')
            kp = command.substring(2).toInt();
        if (command[1] == 'i')
            ki = command.substring(2).toInt();
        if (command[1] == 'd')
            kd = command.substring(2).toInt();

        PID_controller.SetTunings(kd, ki, kd);
    }
}

void set_rpm() {
  /*to send "set speed" command to the slave in address 1 (motor) */

  Wire.beginTransmission(0X01); // address 1 for motor controller
  Wire.write('S'); // S --> set Speed 
  String aux_rpm = String(rpm_value);
  // it is necessary to send character by character
  for(int i =0; i < aux_rpm.length(); i++ ) {
    Wire.write(aux_rpm[i]);
  }
  Wire.endTransmission();
  Serial.print("Speed was set to ");
  Serial.print(rpm_value);
  Serial.println(" rpm");
}

void run_measurement() {
  /*to send "run" command to the slave in address 1 (motor) */
  Serial.println("RUN");
  measure_temp = true;

  // then start the round
  Wire.beginTransmission(0X01);
  Wire.write('R'); // R --> Start the round
  Wire.endTransmission();
}

void reset_motor(){
  // reset the system
  Serial.println("RES");
  measure_temp = false;
  Wire.beginTransmission(0X01); // address 1 for motor controller
  Wire.write('r'); // R --> Start the round
  Wire.endTransmission();
}

void invert_motor(){
  // reset the system
  Serial.println("INV");
  Wire.beginTransmission(0X01); // address 1 for motor controller
  Wire.write('i'); // R --> Start the round
  Wire.endTransmission();
}

void end_measure(){
  measure_temp = false;
  Serial.println("FIN");
}
