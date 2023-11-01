/*Motor code...*/

#include <Wire.h>
#include <Stepper.h>


// pins definition
int enb_pin = 7;
int dir_pin = 8;
int step_pin = 9;
int end0_pin = 2;
int end1_pin= 3;
int signal_end_out = 5;

// auxiliary variables
bool start_round;
int dir = 1; // counterclockwise by default

//
int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);
float maxSpeed = 2.8; // m/min
float minSpeed = 0.05; // m/min
float currentSpeed = 1.0;


void setup(){
  Wire.begin(0x01); // I2C address: 1
  Serial.begin(115200);
  // pins configuration
  pinMode(enb_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(step_pin, OUTPUT);
  pinMode(end0_pin, INPUT_PULLUP);
  pinMode(end1_pin, INPUT_PULLUP);
  pinMode(signal_end_out, OUTPUT);
  digitalWrite(signal_end_out, 0);
  
  pinMode(LED_BUILTIN, OUTPUT);

  // interruptions defined by end of the rounds
  attachInterrupt(digitalPinToInterrupt(end0_pin), reset_system_1, FALLING);
  attachInterrupt(digitalPinToInterrupt(end1_pin), go_back, FALLING);

  Wire.onReceive(controler);
  set_speed(currentSpeed);
}

void loop(){

  if (start_round){
    // motor step pulse
    myStepper.step(1);
  }
}

void controler(){
  // receiving command
  String command = "";

  while(Wire.available()){
    char c = Wire.read();
    command += String(c);
  }

  if (command[0] == 'S'){ // S --> speed
    float desiredSpeed = command.substring(1).toFloat();
    set_speed(command.substring(1).toFloat());
  } 
  if (command[0] == 'R'){ // R --> Run
    start_round = true;
    digitalWrite(enb_pin, 0);
    digitalWrite(LED_BUILTIN, 1); // led running indicator
    Serial.println("RUN");
  }  
  if (command[0] == 'r'){ // r --> reset
    reset_system_2();
  }
  if (command[0] == 'i'){ // i --> invert direction
    go_back();
  }
}

void set_speed(int motor_speed){
  // motor_speed [rpm] = 1.8°/360° * pulse_speed (Hz) * 60 
  // based on https://youtu.be/VCv4PeEWfzQ
  if (motor_speed < minSpeed) {
    motor_speed = minSpeed;
  } else if (motor_speed > maxSpeed) {
    motor_speed = maxSpeed;
  }
  currentSpeed = motor_speed;
  float stepsPerSecond = (currentSpeed / 60) * stepsPerRevolution;
  myStepper.setSpeed(stepsPerSecond);
  Serial.println("Speed set to " + String(currentSpeed) + " m/min");
}

void reset_system_1(){
  Serial.println("FIN");
  digitalWrite(enb_pin, 1); // disable for does not consume current
  dir = 1;
  digitalWrite(dir_pin, dir);

  // produce a pulse to notify master about the resetting of the system
  digitalWrite(signal_end_out, 1);
  delay(10);
  digitalWrite(signal_end_out, 0);
  delay(10);
  digitalWrite(signal_end_out, 1);

  digitalWrite(LED_BUILTIN, 0); // LED running indicator off
  start_round = false;
}

void reset_system_2(){
  Serial.println("RES");
  digitalWrite(enb_pin, 1); // disable for does not consume current
  digitalWrite(dir_pin, dir);

  digitalWrite(LED_BUILTIN, 0); // LED running indicator off
  start_round = false;
}



void go_back(){
  dir = !dir;
  Serial.println("INV " + String(dir));
  digitalWrite(dir_pin, dir); // changing the direction
}
