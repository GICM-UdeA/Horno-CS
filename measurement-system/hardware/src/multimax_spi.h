/*
================================================================
Personalized library to take data from 6 thermocouples connected to the MAX6675 module. 
Each thermocouple communicates with Arduino through SPI protocol, and measurement management 
is handled by the MMAX6675 class (Multi MAX6675).

@author Daniel Estrada
@date 03-2024
================================================================
*/
#ifndef MULTI_MAX6675_SPI_H
#define MULTI_MAX6675_SPI_H

#include "Arduino.h"
#include <ArduinoQueue.h> 
#include "SPI.h"

// Structure to store measurements from 6 thermocouples
typedef struct measure {
    float T1; // Temperature measurement for thermocouple 1
    float T2; // Temperature measurement for thermocouple 2
    float T3; // Temperature measurement for thermocouple 3
    float T4; // Temperature measurement for thermocouple 4
    float T5; // Temperature measurement for thermocouple 5
    float T6; // Temperature measurement for thermocouple 6
} measure;

// Class for handling multiple MAX6675 sensors
class MMAX6675 {
public:
    // Constructor
    MMAX6675(int8_t CS_1, int8_t CS_2, int8_t CS_3, int8_t CS_4, int8_t CS_5, int8_t CS_6, int maxItems);

    // Method to register temperatures
    int regTemperatures(void);

    // Method to retrieve measurements
    String get_measurements();

    // Queue for storing measurements
    ArduinoQueue<measure> dataQueue; // Definition of data Queue

private:
    int8_t cs_pins[6]; // Array to store CS pin numbers
};

#endif
