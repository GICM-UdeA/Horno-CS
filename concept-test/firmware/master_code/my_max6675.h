#ifndef MY_MAX6675_H
#define MY_MAX6675_H

#include "Arduino.h"
#include "SPI.h"

class MY_MAX6675 {
public:
    MY_MAX6675(int8_t CS);

    float readCelsius(void);

    private:
    int8_t cs;
};

#endif
