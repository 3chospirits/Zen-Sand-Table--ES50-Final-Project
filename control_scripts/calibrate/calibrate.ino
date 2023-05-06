// calibrate.ino
// This script is used to move the motors to 0,0 for calibration.
// Both motors will move independently until they hit the 0,0 switch

// TODO: TEST UPDATED CODE
#include <AccelStepper.h>

// motor driver resolution pins
#define MOTOR_X_S1 2
#define MOTOR_X_S2 3
#define MOTOR_X_S3 4
#define MOTOR_Y_S1 5
#define MOTOR_Y_S2 6
#define MOTOR_Y_S3 7

// motor control pins (for motor driver)
#define MOTOR_XA 8
#define MOTOR_XB 9
#define MOTOR_YA 10
#define MOTOR_YB 11

#define SWITCH_X A1
#define SWITCH_Y A0

AccelStepper stepperX(AccelStepper::DRIVER, MOTOR_XA, MOTOR_XB);
AccelStepper stepperY(AccelStepper::DRIVER, MOTOR_YA, MOTOR_YB);

void setup() {
  // setup pin modes
  pinMode(SWITCH_X, INPUT);
  pinMode(SWITCH_Y, INPUT);

  pinMode(MOTOR_XA, OUTPUT);
  pinMode(MOTOR_XB, OUTPUT);
  pinMode(MOTOR_YA, OUTPUT);
  pinMode(MOTOR_YB, OUTPUT);

  pinMode(MOTOR_X_S1, OUTPUT);
  pinMode(MOTOR_X_S2, OUTPUT);
  pinMode(MOTOR_X_S3, OUTPUT);

  pinMode(MOTOR_Y_S1, OUTPUT);
  pinMode(MOTOR_Y_S2, OUTPUT);
  pinMode(MOTOR_Y_S3, OUTPUT);

  // Initialize the stepper motor default values
  stepperX.setCurrentPosition(0); 
  stepperY.setCurrentPosition(0);
  stepperX.setAcceleration(30000);
  stepperY.setAcceleration(30000);

  stepperX.setMaxSpeed(1000);
  stepperY.setMaxSpeed(1000);
  // Guarentee we move to 0,0. The max length of the box is
  // 19400 steps, so this guarentees we'll hit the switch and stop
  stepperX.moveTo(-30000);
  stepperY.moveTo(-30000);

  Serial.begin(9600); // Initialize serial communication
}

bool x_run = true;
bool y_run = true;

// delay startup to get proper readings from switches
bool first = true;

void loop() {
  if (first){
    delay(1000);
    first = false;
  } 

  // set both motor drivers to sixteenth-step resolution (max precision)
  digitalWrite(MOTOR_X_S1, HIGH);
  digitalWrite(MOTOR_X_S2, HIGH);
  digitalWrite(MOTOR_X_S3, HIGH);

  digitalWrite(MOTOR_Y_S1, HIGH);
  digitalWrite(MOTOR_Y_S2, HIGH);
  digitalWrite(MOTOR_Y_S3, HIGH);

  // read the switch values. Pressed = 1023, not pressed = 0
  int x_val = analogRead(SWITCH_X);
  int y_val = analogRead(SWITCH_Y);

  // if the switch is pressed, stop moving the motor
  if (x_val > 10) x_run = false;
  if (y_val > 10) y_run = false;

  // only run each motor if it hasn't hit its corresponding switch yet
  if (x_run){
    stepperX.run();
  }
  if (y_run){
    stepperY.run();
  }
}
