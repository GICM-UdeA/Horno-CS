#include "my_max6675.h"


MY_MAX6675::MY_MAX6675(int8_t CS) {
    cs = CS;
    // define chip select (SC) pin mode
    pinMode(cs, OUTPUT);
    digitalWrite(cs, HIGH);

    SPI.begin();
}


float MY_MAX6675::readCelsius(void) {
    uint16_t v;

    digitalWrite(cs, LOW);

    v=SPI.transfer(0x00);
    v <<= 8;
    v |= SPI.transfer(0x00);

    digitalWrite(cs, HIGH);

    if (v & 0x4) {
        // no thermocouple attached!
        return NAN;
    }

    v >>= 3;

    return v * 0.25;
}