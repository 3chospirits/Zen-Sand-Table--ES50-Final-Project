#include <Stepper.h>
#define STEPS 200 // 250 steps is about 1mm   11.75cm per 25000 16th steps (0.47 mm / 16th step)
#define MOTOR_SPEED 500
// #define MS1 8 // https://lastminuteengineers.com/a4988-stepper-motor-driver-arduino-tutorial/
// #define MS2 9
// #define MS3 10

#define MOTOR1_S1 2
#define MOTOR1_S2 3
#define MOTOR1_S3 4

#define MOTOR2_S1 5
#define MOTOR2_S2 6
#define MOTOR2_S3 7

#define MOTOR1_A 8
#define MOTOR1_B 9

#define MOTOR2_A 10
#define MOTOR2_B 11

Stepper stepper1(STEPS, MOTOR1_A, MOTOR1_B);
Stepper stepper2(STEPS, MOTOR2_A, MOTOR2_B);

// Stepper stepper1(STEPS, 2, 3);
#define motorInterfaceType 1


void setup() {
  stepper1.setSpeed(MOTOR_SPEED);
  stepper2.setSpeed(MOTOR_SPEED);

  pinMode(MOTOR1_S1, OUTPUT);
  pinMode(MOTOR1_S2, OUTPUT);
  pinMode(MOTOR1_S3, OUTPUT);

  pinMode(MOTOR2_S1, OUTPUT);
  pinMode(MOTOR2_S2, OUTPUT);
  pinMode(MOTOR2_S3, OUTPUT);
}

void loop() {
  digitalWrite(MOTOR1_S1, HIGH);
  digitalWrite(MOTOR1_S2, HIGH);
  digitalWrite(MOTOR1_S3, HIGH);

  digitalWrite(MOTOR2_S1, HIGH);
  digitalWrite(MOTOR2_S2, HIGH);
  digitalWrite(MOTOR2_S3, HIGH);
  
  stepper1.step(2*-2500);
  stepper2.step(2*-2500);
  stepper1.step(2*2500);
  stepper2.step(2*2500);

  // stepper1.step(-25000);
  // stepper1.step(25000);

  // stepper2.step(-25000);
  // stepper2.step(25000);

  // delay(1000000);
}

// 13 12 11 motor 1 driver
// 10 9  8  motor 2 driver

// 2  3     motor 1
// 4  5     motor 2 
