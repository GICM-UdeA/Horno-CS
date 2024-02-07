#include "thermocouple.h"

int MAX6675_SO;
int MAX6675_CS;
int MAX6675_SCK;

void set_thermocouple(int PIN_SO = 4, int PIN_CS = 5, int PIN_SCK = 6){
    // setting up thermocouple pins
    
    // Thermocouple pins
    MAX6675_SO = PIN_SO;
    MAX6675_CS = PIN_CS;
    MAX6675_SCK = PIN_SCK;
    
    pinMode(MAX6675_CS, OUTPUT);
    pinMode(MAX6675_SO, INPUT);
    pinMode(MAX6675_SCK, OUTPUT);
}

double measure_temp(){
     // code based on https://electronoobs.com/eng_arduino_tut24.php
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
