/*Motor code...*/

#include <Wire.h>

// pins definition
int enb_pin = 7;
int dir_pin = 8;
int step_pin = 9;
int end0_pin = 2;
int end1_pin= 3;
int signal_end_out = 11;

// auxiliary variables
bool start_round;
long int pulse_duration;

void setup(){
  Wire.begin(0x01); // I2C address: 1

  // pins configuration
  pinMode(enb_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(step_pin, OUTPUT);
  pinMode(end0_pin, INPUT_PULLUP);
  pinMode(end1_pin, INPUT_PULLUP);
  pinMode(signal_end_out, INPUT_PULLUP);
  digitalWrite(signal_end_out, 0);
  
  pinMode(LED_BUILTIN, OUTPUT);

  // resetting system to the original position
  reset_system();

  // interruptions defined by end of the rounds
  attachInterrupt(digitalPinToInterrupt(end0_pin), reset_system, FALLING);
  attachInterrupt(digitalPinToInterrupt(end1_pin), go_back, FALLING);

  Wire.onReceive(controler);
}

void loop(){

  if (start_round){
    // motor step pulse
    digitalWrite(step_pin, HIGH);
    delayMicroseconds(pulse_duration);
    digitalWrite(step_pin, LOW);
    delayMicroseconds(pulse_duration);
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
    set_speed(command.substring(1).toInt());
  } 
  if (command[0] == 'R'){ // R --> Run
    start_round = true;
    digitalWrite(enb_pin, 1);
    digitalWrite(LED_BUILTIN, 1); // led running indicator
  }  
  if (command[0] == 'r'){ // r --> reset
    reset_system();
  }
  if (command[0] == 'i'){ // i --> invert direction
    go_back();
  }
}

void set_speed(int motor_speed){
  // motor_speed [rpm] = 1.8°/360° * pulse_speed (Hz) * 60 
  // based on https://youtu.be/VCv4PeEWfzQ
  double pulse_speed = 200 * motor_speed * 1/60.0; // rpm

  // changing to microseconds
  pulse_duration = int(1000000 / pulse_speed); 
}

void reset_system(){
  digitalWrite(enb_pin, 0); // disable for does not consume current
  digitalWrite(dir_pin, 0);// counterclockwise by default

  // produce a pulse to notify master about the resetting of the system
  digitalWrite(signal_end_out, 1); 
  digitalWrite(signal_end_out, 0);

  digitalWrite(LED_BUILTIN, 0); // LED running indicator off
  start_round = false;
}

void go_back(){
  digitalWrite(dir_pin, 1); // changing the direction
}
