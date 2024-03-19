#include "multimax_spi.h"

#define T1_CS_PIN  4
#define T2_CS_PIN  5
#define T3_CS_PIN  6
#define T4_CS_PIN  7
#define T5_CS_PIN  8
#define T6_CS_PIN  9

// Instantiate MMAX6675 object with the specified chip select (CS) pins and maximum queue size
MMAX6675 measure_system(T1_CS_PIN, T2_CS_PIN, T3_CS_PIN, T4_CS_PIN, T5_CS_PIN, T6_CS_PIN, 200);

// Variables for controlling the measurement process
bool start = 0; // Flag to indicate whether measurements should be started or stopped
long int Time, prevTime; // Variables to keep track of time
unsigned long samplingTime = 1000; // Default sampling time (milliseconds), initially set to 1 second

void setup()
{
    // Initialize serial communication
    Serial.begin(115200);

    // Initialize previous time
    prevTime = millis();
}

void loop()
{   
    // If measurement process is started
    if (start){
        // Get current time
        Time = millis();

        // Check if it's time to take a new measurement (every 1000 milliseconds)
        if (Time - prevTime > 1000){
            // Register temperatures and check if successful
            if (!measure_system.regTemperatures()){
                // Print error message if registration fails
                Serial.println("BF"); // Error code BF (Buffer Full)
                start = 0; // Stop measurement process
            }
            prevTime = Time; // Update previous time
        }
    }
}

// Function to handle serial events (incoming commands)
void serialEvent(){
    String command = Serial.readStringUntil('\n'); // Read incoming command from serial port
    command.trim(); // Remove leading and trailing whitespaces

    // Process incoming commands
    if (command == "start"){
        start = 1; // Start measurement process
    }
    if (command == "stop"){
        start = 0; // Stop measurement process
    }
    if (command == "get"){
        // Check if data queue is not empty
        if (!measure_system.dataQueue.isEmpty())
            Serial.println(measure_system.get_measurements()); // Get and print measurements
        else
            Serial.println("BE"); // Error code BE (Buffer Empty)
    }
    if (command.startsWith("set_time")) {
        // Extract sampling time from the command
        int newSamplingTime = command.substring(8).toInt(); // The format should be "set_time XXX" where XXX is the new sampling time

        // Check if the new sampling time is at least 250 ms
        if (newSamplingTime >= 250) {
            samplingTime = newSamplingTime; // Update sampling time
            Serial.println("SOK"); // Sampling time OK.
        } else {
            Serial.println("SNOK"); // Error code SNOK (Sampling time no OK)
        }
    }
}
