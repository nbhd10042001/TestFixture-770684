#include <libcustom_758239.h>

#ifndef TestStep_758239
#define TestStep_758239

class TS_758239
{
public:
    static libcustom_758239 customLib;
    TS_758239();
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

#endif // TestStep_758239
