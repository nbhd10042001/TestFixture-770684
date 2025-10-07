#include <libcustom_758239.h>

const int sampleCount = 10; // sample for analogRead
String delimiter = "-";

libcustom_758239::libcustom_758239()
{
    initPinDigital();
    initPinAnalog();
}

void libcustom_758239::initPinDigital()
{
  int len1 = sizeof(DigitalOutputs) / sizeof(DigitalOutputs[0]);
  for (int i = 0; i < len1; i++)
    pinMode(DigitalOutputs[i], OUTPUT);

  int len2 = sizeof(DigitalInput) / sizeof(DigitalInput[0]);
  for (int i = 0; i < len2; i++)
    pinMode(DigitalInput[i], INPUT);
}

void libcustom_758239::initPinAnalog()
{
  int len = sizeof(AnalogInputs) / sizeof(AnalogInputs[0]);
  for (int i = 0; i < len; i++)
    pinMode(AnalogInputs[i], INPUT);
}

float libcustom_758239::caculateVoltageReadFromADC(int pin)
{
  int adcValue = analogReadWithSample(pin);
  float voltage = (adcValue * Vcc) / resolutionADC;
  return voltage;
}

float libcustom_758239::analogReadWithSample(int pin)
{
  long total = 0;
  float value = 0;
  for (int i = 0; i < sampleCount; i++)
  {
    value = analogRead(pin);
    if(i == 0 || i == 1) // bỏ qua 2 giá trị đầu tiên
      continue;
    total += value;
    delay(5); 
  }
  return total / sampleCount;
}

void libcustom_758239::resetActiveRelay()
{
  digitalWrite(D5, LOW);
  digitalWrite(D6, LOW);
  digitalWrite(D7, LOW);
  digitalWrite(D8, HIGH);
  digitalWrite(D9, LOW);
  digitalWrite(D14, LOW);
  digitalWrite(D51, LOW);
}

bool libcustom_758239::checkStopTest()
{
  for (int i = 0; i < 30; i++)
  {
    if (Serial.available() > 0)
    {
      String input = Serial.readStringUntil('\n');
      input.trim(); // xóa ký tự trắng, \r, \n dư thừa
      if (input == "stop" || input == "stop program")
      {
        resetActiveRelay();
        Serial.println("STOP");
        return true;
      }
    }
    delay(10);
  }
  return false;
}