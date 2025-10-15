/*  
  This is a gui for test fixture board 770684, a unique product of Saigon Fab-9
  Do not copy or distribute this code
  Author by Duc Nguyen
  Version 1.0
*/

#include <TestStep_770684.h>
String data_receive = "";
char buffer[50];

TS_770684 ts_770684;
void startTest();
void startAutoTest();

void setup()
{
  Serial.begin(115200);
  analogReference(DEFAULT);
}

void loop()
{
  // read data serial from GUI
  if (Serial.available() > 0)
  {
    data_receive = Serial.readStringUntil('\n');
    data_receive.trim();
    if (data_receive == "stop")
    {
      ts_770684.customLib.resetActiveRelay();
      return;
    }
    if (data_receive == "auto")
      startAutoTest();
    if (data_receive == "start")
      startTest();
    // ts_770684.customLib.resetActiveRelay();
    delay(50);
  }
}

void startTest()
{
  String input, command;
  int value = 0;
  while (data_receive == "start")
  {
    if (Serial.available() > 0)
    {
      String data = Serial.readStringUntil('\n');
      data.trim();
      if (data == "stop" || data == "stop program")
      {
        Serial.println("STOP");
        ts_770684.customLib.resetActiveRelay();
        break;
      }

      int separatorIndex = data.indexOf('-'); // Vị trí dấu '-'

      if (separatorIndex != -1)
      {
        command = data.substring(0, separatorIndex);        // Từ đầu đến trước '-'
        value = data.substring(separatorIndex + 1).toInt(); // Từ sau '-' đến hết
      }
      Serial.println("Command: " + command + ", Value: " + String(value));

      if (command == "run" && value > 0 && value < 9)
      {
        if (value == 1)
          ts_770684.test_Step1();
        else if (value == 2)
          ts_770684.test_Step2();
        else if (value == 3)
          ts_770684.test_Step3();
        else if (value == 4)
          ts_770684.test_Step4();
        else if (value == 5)
          ts_770684.test_Step5();
        else if (value == 6)
          ts_770684.test_Step6();
        else if (value == 7)
          ts_770684.test_Step7();
        else if (value == 8)
          ts_770684.test_Step8();
      }
    }
    delay(10);
  }
}

void startAutoTest()
{
  ts_770684.currentStep = 1;
  while (data_receive == "auto")
  {
    data_receive = "";                      // reset data_receive to empty string
    ts_770684.customLib.resetActiveRelay(); // reset all relay
    Serial.println("[System log] Starting Test for 75839...");
    delay(500);

    if (ts_770684.currentStep == 1)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step1();
    }

    if (ts_770684.currentStep == 2)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step2();
    }

    if (ts_770684.currentStep == 3)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step3();
    }

    if (ts_770684.currentStep == 4)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step4();
    }

    if (ts_770684.currentStep == 5)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step5();
    }

    if (ts_770684.currentStep == 6)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step6();
    }

    if (ts_770684.currentStep == 7)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step7();
    }

    if (ts_770684.currentStep == 8)
    {
      if (ts_770684.customLib.checkStopTest())
        break;
      ts_770684.test_Step8();
    }

    // final result
    int countFail = 0;
    int len = sizeof(ts_770684.steps) / sizeof(ts_770684.steps[0]);
    String msg = "FAIL";
    for (int i = 0; i < len; i++)
    {
      if (ts_770684.steps[i] == 0)
      {
        msg = msg + "-" + String(i);
        countFail++;
      }
    }
    if (countFail > 0)
      Serial.println(msg);
    if (countFail == 0)
      Serial.println("PASS");
  }
}
