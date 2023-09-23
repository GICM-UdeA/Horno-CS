/* I2C master code...*/

#include "max6675.h" // amplifier module for the Thermocouple
#include <Wire.h> // for I2C comunication

// Thermocouple pins
const int MAX6675_SO = 4;
const int MAX6675_CS = 5;
const int MAX6675_SCK = 6;

// to enable the measurement
volatile bool measure_temp = false;

// to stop the measurement
const int end_pin = 3;

// speed variable
int rpm_value = 0;

void setup() {
  // setting up thermocouple pins
  pinMode(MAX6675_CS, OUTPUT);
  pinMode(MAX6675_SO, INPUT);
  pinMode(MAX6675_SCK, OUTPUT);
  pinMode(3, INPUT);
  Serial.begin(115200);
  Wire.begin();

  attachInterrupt(digitalPinToInterrupt(end_pin), end_measure, FALLING);
}

void loop() {
  if (measure_temp){
    Serial.println(readThermocouple());
    delay(250);
  }
}

void serialEvent() {
  /*Command codification*/
  
  String command = Serial.readString();
  
  if (command[0] == 'S'){ // S --> to set the speed (in rpm)
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

double readThermocouple() {
  // code taken from https://electronoobs.com/eng_arduino_tut24.php
  uint16_t v;
  
  digitalWrite(MAX6675_CS, LOW);
  delay(1);

  // Read in 16 bits,
  //  15    = 0 always
  //  14..2 = 0.25 degree counts MSB First
  //  2     = 1 if thermocouple is open circuit  
  //  1..0  = uninteresting status
  
  v = shiftIn(MAX6675_SO, MAX6675_SCK, MSBFIRST);
  v <<= 8;
  v |= shiftIn(MAX6675_SO, MAX6675_SCK, MSBFIRST);
  
  digitalWrite(MAX6675_CS, HIGH);
  if (v & 0x4) 
  {    
    // Bit 2 indicates if the thermocouple is disconnected
    return NAN;     
  }

  // The lower three bits (0,1,2) are discarded status bits
  v >>= 3;

  // The remaining bits are the number of 0.25 degree (C) counts
  return v*0.25;
}
