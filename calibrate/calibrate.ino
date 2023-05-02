// Green = X
// Blue = Y
// Continuously runs each motor until we reach 0,0.

#include <AccelStepper.h>
#define STEPS 200 // 250 steps is about 1mm   11.75cm per 25000 16th steps (0.47 mm / 16th step)

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

#define SWITCH_X A1
#define SWITCH_Y A0

AccelStepper stepperX(AccelStepper::DRIVER, MOTOR1_A, MOTOR1_B);
AccelStepper stepperY(AccelStepper::DRIVER, MOTOR2_A, MOTOR2_B);

void setup() {
  pinMode(SWITCH_X, INPUT);
  pinMode(SWITCH_Y, INPUT);

  pinMode(MOTOR1_A, OUTPUT);
  pinMode(MOTOR1_B, OUTPUT);
  pinMode(MOTOR2_A, OUTPUT);
  pinMode(MOTOR2_B, OUTPUT);

  pinMode(MOTOR1_S1, OUTPUT);
  pinMode(MOTOR1_S2, OUTPUT);
  pinMode(MOTOR1_S3, OUTPUT);

  pinMode(MOTOR2_S1, OUTPUT);
  pinMode(MOTOR2_S2, OUTPUT);
  pinMode(MOTOR2_S3, OUTPUT);

  Serial.begin(9600);
  stepperX.setCurrentPosition(0); 
  stepperY.setCurrentPosition(0);
  stepperX.setAcceleration(30000);
  stepperY.setAcceleration(30000);

  stepperX.setMaxSpeed(3000);
  stepperY.setMaxSpeed(3000);
  stepperX.moveTo(-30000);
  stepperY.moveTo(-30000);
}

bool x_run = true;
bool y_run = true;

bool first = true;

void loop() {
  if (first){
    delay(1000);
    first = false;
  } 
  digitalWrite(MOTOR1_S1, HIGH);
  digitalWrite(MOTOR1_S2, HIGH);
  digitalWrite(MOTOR1_S3, HIGH);

  digitalWrite(MOTOR2_S1, HIGH);
  digitalWrite(MOTOR2_S2, HIGH);
  digitalWrite(MOTOR2_S3, HIGH);

  int x_val = analogRead(SWITCH_X);
  int y_val = analogRead(SWITCH_Y);

  if (x_val > 10) x_run = false;
  if (y_val > 10) y_run = false;

  if (x_run){
    // Serial.print("X running ");
    stepperX.run();
  }
  // else Serial.println("X stopped ");
  if (y_run){
    // Serial.print("Y running");
    stepperY.run();
  }
  // else Serial.println("Y stopped");

  // Serial.println("");
}
