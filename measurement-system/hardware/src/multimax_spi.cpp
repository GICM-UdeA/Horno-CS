#include "multimax_spi.h"

// Constructor of the MMAX6675 class
MMAX6675::MMAX6675(int8_t CS_1, int8_t CS_2, int8_t CS_3, int8_t CS_4, int8_t CS_5, int8_t CS_6, int maxItems):
    dataQueue(maxItems) // Initialization of dataQueue with the specified maximum size
{
    // Initialization of chip select (CS) pins
    for (int i = 0; i <= 5; i++)
        pinMode(cs_pins[i], OUTPUT); // Set pin mode to output

    // Initialize CS pins as inactive (HIGH) to deactivate SPI devices
    for (int i = 0; i <= 5; i++)
        digitalWrite(cs_pins[i], HIGH);

    SPI.begin(); // Initialize the SPI bus
}

// Method to register temperatures
int MMAX6675::regTemperatures(void) {
    uint16_t vals[6]; // Array to store raw values read from the sensors
    float out_vals[6]; // Array to store converted temperatures

    // Read raw values from the sensors
    for (int i = 0; i <= 5; i++){
        digitalWrite(cs_pins[i], LOW); // Select sensor i

        // Read data from the sensor (16 bits)
        vals[i] = SPI.transfer(0x00);
        vals[i] <<= 8;
        vals[i] |= SPI.transfer(0x00);

        digitalWrite(cs_pins[i], HIGH); // Deselect sensor i
    }

    // Convert raw values to temperatures
    for (int i = 0; i <= 5; i++){
        if (vals[i] & 0x4) // Check if no thermocouple is attached
            vals[i] = NAN; // If no thermocouple, assign a NAN (Not a Number) value
        else
            vals[i] >>= 3; // Bit shifting to get temperature in Celsius

        out_vals[i] =  vals[i] * 0.25; // Conversion to Celsius
    }

    // If the queue is not full, enqueue the new temperature measurement
    if (! dataQueue.isFull()){
        measure data = {out_vals[0],out_vals[1],out_vals[2], out_vals[3], out_vals[4],out_vals[5]}; 
        dataQueue.enqueue(data); // Enqueue the new temperature measurement
        return 1; // Return 1 to indicate that a new measurement has been registered
    }
    else 
        return 0; // Return 0 to indicate that the queue is full and the new measurement could not be registered
}

// Method to get measurements in JSON string format
String MMAX6675::get_measurements(){
    measure data = dataQueue.dequeue(); // Extract the oldest measurement from the queue
    // Create a JSON string with the measurements
    String message = 
        "{\"T1\":" + String(data.T1) + ","
        + "\"T2\":" + String(data.T2) + ","
        + "\"T3\":" + String(data.T3) + ","
        + "\"T4\":" + String(data.T4) + ","
        + "\"T5\":" + String(data.T5) + ","
        + "\"T6\":" + String(data.T6) + "}";

    return message; // Return the JSON string with the measurements
}
