#include <libcustom_770684.h>

#ifndef TestStep_770684
#define TestStep_770684

class TS_770684
{
public:
    static libcustom_770684 customLib;
    TS_770684();
    void test_Step1();
    void test_Step2();
    void test_Step3();
    void test_Step4();
    void test_Step5();
    void test_Step6();
    void test_Step7();
    void test_Step8();
    int steps[9] = {
        -1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    };
    int currentStep = 0;
};

#endif // TestStep_770684
