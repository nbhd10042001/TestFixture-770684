#include <TestStep_758239.h>
String data_receive = "";
char buffer[50];

TS_758239 ts_758239;
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
      ts_758239.customLib.resetActiveRelay();
      return;
    }
    if (data_receive == "auto")
      startAutoTest();
    if (data_receive == "start")
      startTest();
    // ts_758239.customLib.resetActiveRelay();
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
        ts_758239.customLib.resetActiveRelay();
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
          ts_758239.test_Step1();
        else if (value == 2)
          ts_758239.test_Step2();
        else if (value == 3)
          ts_758239.test_Step3();
        else if (value == 4)
          ts_758239.test_Step4();
        else if (value == 5)
          ts_758239.test_Step5();
        else if (value == 6)
          ts_758239.test_Step6();
        else if (value == 7)
          ts_758239.test_Step7();
        else if (value == 8)
          ts_758239.test_Step8();
      }
    }
    delay(10);
  }
}

void startAutoTest()
{
  ts_758239.currentStep = 1;
  while (data_receive == "auto")
  {
    data_receive = "";                      // reset data_receive to empty string
    ts_758239.customLib.resetActiveRelay(); // reset all relay
    Serial.println("[System log] Starting Test for 75839...");
    delay(500);

    if (ts_758239.currentStep == 1)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step1();
    }

    if (ts_758239.currentStep == 2)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step2();
    }

    if (ts_758239.currentStep == 3)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step3();
    }

    if (ts_758239.currentStep == 4)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step4();
    }

    if (ts_758239.currentStep == 5)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step5();
    }

    if (ts_758239.currentStep == 6)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step6();
    }

    if (ts_758239.currentStep == 7)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step7();
    }

    if (ts_758239.currentStep == 8)
    {
      if (ts_758239.customLib.checkStopTest())
        break;
      ts_758239.test_Step8();
    }

    // final result
    int countFail = 0;
    int len = sizeof(ts_758239.steps) / sizeof(ts_758239.steps[0]);
    String msg = "FAIL";
    for (int i = 0; i < len; i++)
    {
      if (ts_758239.steps[i] == 0)
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
