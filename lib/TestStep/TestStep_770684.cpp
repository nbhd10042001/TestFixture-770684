#include <TestStep_770684.h>

const int R1 = 10000; // 10k ohm
const int R2 = 1200;  // 1.2k ohm
const float Vi_1 = 24.0;  // 24V
const float Vo_1 = (Vi_1 * R2) / (R1 + R2);
const float Vi_2 = 5.0;   // 5V
const float Vo_2 = (Vi_2 * R2) / (R1 + R2);

String message = "";
const String status[2] = {"[Fail]", "[Pass]"};
libcustom_770684 customLib;

libcustom_770684 TS_770684::customLib;
TS_770684::TS_770684() {}

// first char is step type: P-pass, F-fail, S-start, E-end

void TS_770684::test_Step1()
{
    // Serial.println("[System Log] Step 1 processing");
    Serial.println("S-1-0");
    digitalWrite(D14, HIGH);
    if (digitalRead(D14) == 1)
    {
        // Serial.println("---[Pass] Active relay and apply 0v for J1-4/J1-6 success!");
        Serial.println("P-1-1");
        delay(700);
        bool isFail = false;

        int value = digitalRead(D48);
        // message = "---" + (value == 0 ? status[1] : status[0]) + " Value digital D48 (J13-10): " + (value == 1 ? "High" : "Low") + " (expect : Low)";
        message = (value == 0 ? "P-1-2-low" : "F-1-2-high");
        if (value == 1)
            isFail = true;
        Serial.println(message);
        delay(100);

        value = digitalRead(D53);
        // message = "---" + (value == 0 ? status[1] : status[0]) + " Value digital D53 (J13-5): " + (value == 1 ? "High" : "Low") + " (expect : Low)";
        message = (value == 0 ? "P-1-3-low" : "F-1-3-high");
        if (value == 1)
            isFail = true;
        Serial.println(message);
        delay(100);
        if (isFail)
            steps[1] = 0;
        else
            steps[1] = 1;
    }
    else
    {
        steps[1] = 0;
        // Serial.println("---[Fail] Active relay and apply 0v for J1-4/J1-6 fail!");
        Serial.println("F-1-1");
        delay(100);
    }
    // Serial.println("[System Log] Step 1 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-1-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step2()
{
    // Serial.println("[System Log] Step 2 processing");
    Serial.println("S-2-0");
    digitalWrite(D7, HIGH);
    if (digitalRead(D7) == 1)
    {
        // Serial.println("---[Pass] Turn on PSW1 success!");
        Serial.println("P-2-1");
        delay(700);
        steps[2] = 1;
    }
    else
    {
        // Serial.println("---[Fail] Turn on PSW1 fail!");
        Serial.println("F-2-1");
        delay(100);
        steps[2] = 0;
    }
    // Serial.println("[System Log] Step 2 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-2-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step3()
{
    // Serial.println("[System Log] Step 3 processing");
    Serial.println("S-3-0");
    digitalWrite(D6, HIGH);
    if (digitalRead(D6) == 1)
    {
        // Serial.println("---[Pass] Active relay and apply 24v for J43/J44 success!");
        Serial.println("P-3-1");
        delay(700);

        bool isFail = false;
        float vol = customLib.caculateVoltageReadFromADC(adc1);
        // message = "---" + ((0 <= vol && vol < 0.3) ? status[1] : status[0]) + " Voltage adc 1 (J13-13): " + String(vol) + "V (expect : 0V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = (0 <= vol && vol < 0.3) ? "P-3-2-" + String(vol) : "F-3-2-" + String(vol);
        if (vol > 0.3)
            isFail = true;
        Serial.println(message);
        delay(50);

        vol = customLib.caculateVoltageReadFromADC(adc2);
        // message = "---" + ((0 <= vol && vol < 0.3) ? status[1] : status[0]) + " Voltage adc 2 (J13-12): " + String(vol) + "V (expect : 0V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = (0 <= vol && vol < 0.3) ? "P-3-3-" + String(vol) : "F-3-3-" + String(vol);
        if (vol > 0.3)
            isFail = true;
        Serial.println(message);
        delay(50);

        vol = customLib.caculateVoltageReadFromADC(adc4);
        // message = "---" + ((0 <= vol && vol < 0.3) ? status[1] : status[0]) + " Voltage adc 4 (J13-6): " + String(vol) + "V (expect : 0V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = (0 <= vol && vol < 0.3) ? "P-3-4-" + String(vol) : "F-3-4-" + String(vol);
        if (vol > 0.3)
            isFail = true;
        Serial.println(message);
        delay(50);

        if (isFail)
            steps[3] = 0;
        else
            steps[3] = 1;
    }
    else
    {
        // Serial.println("---[Fail] Active relay and apply 24v for J43/J44 fail!");
        Serial.println("F-3-1");
        delay(100);
        steps[3] = 0;
    }
    // Serial.println("[System Log] Step 3 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-3-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step4()
{
    // Serial.println("[System Log] Step 4 processing");
    Serial.println("S-4-0");
    /*  theo thiết kế thì relay chưa kích thì chân j42-1 và j42-2 sẽ thông nhau, tương tự với j41-1 và j41-2
        phải bật relay thì mới ngắt mạch */
    digitalWrite(D8, LOW);
    if (digitalRead(D8) == 0)
    {
        // Serial.println("---[Pass] Active relay and apply 24v for J41-2/J42-2 success!");
        Serial.println("P-4-1");
        delay(700);

        float vol = customLib.caculateVoltageReadFromADC(adc3);
        // message = "---" + ((0 <= vol && vol < 0.3) ? status[1] : status[0]) + " Voltage adc 3 (J13-11): " + String(vol) + "V (expect : 0V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = (0 <= vol && vol < 0.3) ? "P-4-2-" + String(vol) : "F-4-2-" + String(vol);
        Serial.println(message);
        delay(100);
        if (0 <= vol && vol <= 0.3)
            steps[4] = 1;
        else
            steps[4] = 0;
        delay(100);
    }
    else
    {
        // Serial.println("---[Fail] Active relay and apply 24v for J41-2/J42-2 fail!");
        Serial.println("F-4-1");
        delay(100);
        steps[4] = 0;
    }
    // Serial.println("[System Log] Step 4 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-4-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step5()
{
    // Serial.println("[System Log] Step 5 processing");
    Serial.println("S-5-0");
    digitalWrite(D9, HIGH);
    if (digitalRead(D9) == 1)
    {
        // Serial.println("---[Pass] Active relay and apply 24v for J37-5/J38-5 success!");
        Serial.println("P-5-1");
        delay(700);
        bool isFail = false;
        int value = digitalRead(D2);
        // message = "---" + (value == 1 ? status[1] : status[0]) + " Value digital D2 (J2-1): " + (value == 1 ? "High" : "Low") + " (expect : High)";
        message = (value == 1 ? "P-5-2-high" : "F-5-2-low");
        if (value != 1)
            isFail = true;
        Serial.println(message);
        delay(100);

        value = digitalRead(D4);
        // message = "---" + (value == 1 ? status[1] : status[0]) + " Value digital D4 (J2-5): " + (value == 1 ? "High" : "Low") + " (expect : High)";
        message = (value == 1 ? "P-5-3-high" : "F-5-3-low");
        if (value != 1)
            isFail = true;
        Serial.println(message);
        delay(100);

        if (isFail)
            steps[5] = 0;
        else
            steps[5] = 1;
        delay(100);
    }
    else
    {
        // Serial.println("---[Fail] Active relay and apply 24v for J37-5/J38-5 fail!");
        Serial.println("F-5-1");
        delay(100);
        steps[5] = 0;
    }
    // Serial.println("[System Log] Step 5 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-5-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step6()
{
    // Serial.println("[System Log] Step 6 processing");
    Serial.println("S-6-0");
    digitalWrite(D5, HIGH);
    if (digitalRead(D5) == 1)
    {
        // Serial.println("---[Pass] Active relay and apply 24v for J40-6/J40-4 success!");
        Serial.println("P-6-1");
        delay(700);

        float vol = customLib.caculateVoltageReadFromADC(adc0);
        // message = "---" + ((0 <= vol && vol < 0.3) ? status[1] : status[0]) + " Voltage adc 0 (J13-14): " + String(vol) + "V (expect : 0V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = (0 <= vol && vol < 0.3) ? "P-6-2-" + String(vol) : "F-6-2-" + String(vol);
        Serial.println(message);
        delay(100);
        if (0 <= vol && vol < 0.3)
            steps[6] = 1;
        else
            steps[6] = 0;
    }
    else
    {
        // Serial.println("---[Fail] Active relay and apply 24v for J40-6/J40-4 fail!");
        Serial.println("F-6-1");
        delay(100);
        steps[6] = 0;
    }
    // Serial.println("[System Log] Step 6 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-6-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step7()
{
    // Serial.println("[System Log] Step 7 processing");
    Serial.println("S-7-0");
    digitalWrite(D51, HIGH);
    if (digitalRead(D51) == 1)
    {
        // Serial.println("---[Pass] Active relay and apply 0V for J13-8 success!");
        Serial.println("P-7-1");
        delay(700);

        float vol = customLib.caculateVoltageReadFromADC(adc5);
        // message = "---" + (((Vo_2 - 0.3) < vol && vol < (Vo_2 + 0.3)) ? status[1] : status[0]) + " Voltage adc 5 (J13-4): " + String(vol) + "V (expect :" + String(Vo_2) + "V) (Real Voltage: " + String((vol * (R1 + R2)) / R2) + "V)";
        message = ((Vo_2 - 0.3) < vol && vol < Vo_2) ? "P-7-2-" + String(vol) : "F-7-2-" + String(vol);
        Serial.println(message);
        delay(100);
        if ((Vo_2 - 0.3) < vol && vol < Vo_2)
            steps[7] = 1;
        else
            steps[7] = 0;
    }
    else
    {
        // Serial.println("---[Fail] Active relay and apply 0V for J13-8 fail!");
        Serial.println("F-7-1");
        delay(100);
        steps[7] = 0;
    }
    // Serial.println("[System Log] Step 7 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-7-0");
    delay(100);
    currentStep++;
}

void TS_770684::test_Step8()
{
    // Serial.println("[System Log] Step 8 processing");
    Serial.println("S-8-0");
    // đảm bảo rằng D9 bật để kích relay cung cấp 24V cho J38-5 (spare2)
    if (digitalRead(D9) == 1)
    {
        Serial.println("P-8-1");
        int value = digitalRead(D3);
        // message = value == 1 ? "---[Pass] Value digital D3 (J2-4): High (expect : High)" : "---[Fail] Value digital D3 (J2-4): Low (expect : High)";
        message = value == 1 ? "P-8-2-high" : "F-8-2-low";
        Serial.println(message);
        delay(100);
        if (value == 1)
            steps[8] = 1;
        else
            steps[8] = 0;
    }
    else
    {
        // Serial.println("---[Fail] D9 is not active!");
        Serial.println("F-8-1");
        delay(100);
        steps[8] = 0;
    }
    // Serial.println("[System Log] Step 8 complete !");
    // Serial.println("_______________________________________________");
    Serial.println("E-8-0");
    delay(100);
    currentStep = 0;
}