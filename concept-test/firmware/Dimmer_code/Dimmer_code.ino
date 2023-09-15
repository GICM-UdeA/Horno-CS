int duty_cycle = 0;

void setup() {
  // put your setup code here, to run once:
  pwm_setup();
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    duty_cycle = Serial.parseInt();
    Serial.println(duty_cycle);
    digitalWrite(9, duty_cycle);
  }
  delay(10);
}

void pwm_setup() {
  cli();
  //Set Timer mode
  TCCR1B |= 1<<WGM12;
  TCCR1B &= ~(1<<WGM13);
  TCCR1A |= (1<<WGM10) | (1<<WGM11);

  // Set pwm mode NON INVERSE MODE
  TCCR1A |= 1<<COM1A1;
  TCCR1A &= ~(1<<COM1A0);

  // Set the timer preescalar for the PWM frecuency
  // 16 Mhz / 256 ~ 60 Hz
  TCCR1B &= ~(1<<CS10);
  TCCR1B &= ~(1<<CS11);
  TCCR1B |= 1<<CS12;

  // configure the output compare pin as O/P
  DDRB |= 1<<DDB1;
  // set the duty cycle
  OCR1A = duty_cycle; //0-1023 //50%
  sei();
}
