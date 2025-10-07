#include <Arduino.h>

#ifndef LIBCUSTOM_758239_H
#define LIBCUSTOM_758239_H

const int D2 = 2;
const int D3 = 3;
const int D4 = 4;
const int D5 = 5;
const int D6 = 6;
const int D7 = 7;
const int D8 = 8;
const int D9 = 9;
const int D14 = 14;
const int D48 = 48;
const int D51 = 51;
const int D53 = 53;
const int DigitalInput[5] = {D2, D3, D4, D48, D53};
const int DigitalOutputs[7] = {D5, D6, D7, D8, D9, D14, D51};

const int adc0 = A0;
const int adc1 = A1;
const int adc2 = A2;
const int adc3 = A3;
const int adc4 = A4;
const int adc5 = A5;
const int AnalogInputs[6] = {adc0, adc1, adc2, adc3, adc4, adc5};

const float Vcc = 5.0;
const int resolutionADC = 1024;

class libcustom_758239
{
public:
    libcustom_758239();           // Constructor
    void initPinDigital();        // Initialize digital pins
    void initPinAnalog();         // Initialize analog pins
    float analogReadWithSample(int pin);
    void resetActiveRelay();
    bool checkStopTest();
    float caculateVoltageReadFromADC(int pin);
};

#endif // LIBCUSTOM_758239_H