double duty_cycle = 50.0;
long int cycle_p = 8334;
long int cycle_m= 8334;

void setup(){
  pinMode(9, OUTPUT);  
  Serial.begin(115200);
}

void loop(){
    digitalWrite(9, HIGH);
    delayMicroseconds(cycle_p);
    digitalWrite(9, LOW);
    delayMicroseconds(cycle_m);
}

void serialEvent(){
  duty_cycle = Serial.parseInt() / 100.0;
  cycle_p = long(16667 * duty_cycle);
  cycle_m = long(16667 * (1 - duty_cycle));
}
