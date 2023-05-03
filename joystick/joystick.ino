#include <AccelStepper.h>

#define HORIZONTAL A5
#define VERTICAL A4

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

#define SWITCH_X A0
#define SWITCH_Y A1

AccelStepper stepperX(AccelStepper::DRIVER, MOTOR1_A, MOTOR1_B);
AccelStepper stepperY(AccelStepper::DRIVER, MOTOR2_A, MOTOR2_B);

void setup() {
  pinMode(SWITCH_X, INPUT);
  pinMode(SWITCH_Y, INPUT);
  pinMode(HORIZONTAL, INPUT);
  pinMode(VERTICAL, INPUT);


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

  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  stepperX.setAcceleration(30000);
  stepperY.setAcceleration(30000);
  stepperX.setMaxSpeed(5000);
  stepperY.setMaxSpeed(5000);

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  digitalWrite(MOTOR1_S1, HIGH);
  digitalWrite(MOTOR1_S2, HIGH);
  digitalWrite(MOTOR1_S3, HIGH);

  digitalWrite(MOTOR2_S1, HIGH);
  digitalWrite(MOTOR2_S2, HIGH);
  digitalWrite(MOTOR2_S3, HIGH);

  int V = analogRead(VERTICAL); // Read analog input from A4
  int H = analogRead(HORIZONTAL); // Read analog input from A5

  int x = map(H, 0, 660, -100, 100);
  if (H >= 330 && H <= 338) {
    x = 0;
  }

  int y = map(V, 0, 660, -100, 100);
  if (V >= 319 && V <= 327) {
    y = 0;
  }

  // stepperX.moveTo(stepperX.currentPosition() + x*100);
  // stepperY.moveTo(stepperY.currentPosition() + y*100);

  stepperX.setSpeed(x*100);
  stepperY.setSpeed(y*100);

  // Serial.print("X: ");
  // Serial.print(x);
  // Serial.print("\tY: ");
  // Serial.println(y);

  // delay(100); // Wait for 500ms before repeating the loop
  stepperX.runSpeed();
  stepperY.runSpeed();
}

// Max 661 up & right
// Min 0
// Vert Mid: 323
// Horizontal Mid: 334

