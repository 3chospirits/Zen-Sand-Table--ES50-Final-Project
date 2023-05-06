// joystick.ino
// Script uses joystick input to conrol direction and speed of
// the stepper motors

// TODO: TEST UPDATED CODE
#include <AccelStepper.h>

// joystick input pins
#define HORIZONTAL A5
#define VERTICAL A4

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

// joystick constants
#define JOYSTICK_MAX 660
#define JOYSTICK_MIN 0
#define JOYSTICK_MID_X 325
#define JOYSTICK_MID_Y 335
#define JOYSTICK_TOLERANCE 15
// mid constants used for determining what joystick is at default (no movement)
// tolerance is used to account for noise (or drift) in the joystick

#define MOTOR_SPEED_MAX 5000

// stepper motors
AccelStepper stepperX(AccelStepper::DRIVER, MOTOR_XA, MOTOR_XB);
AccelStepper stepperY(AccelStepper::DRIVER, MOTOR_YA, MOTOR_YB);

void setup() {
  // setup pin modes
  pinMode(HORIZONTAL, INPUT);
  pinMode(VERTICAL, INPUT);

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
  stepperX.setMaxSpeed(MOTOR_SPEED_MAX);
  stepperY.setMaxSpeed(MOTOR_SPEED_MAX);
  stepperX.setSpeed(0);
  stepperY.setSpeed(0);

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // set both motor drivers to sixteenth-step resolution (max precision)
  digitalWrite(MOTOR_X_S1, HIGH);
  digitalWrite(MOTOR_X_S2, HIGH);
  digitalWrite(MOTOR_X_S3, HIGH);

  digitalWrite(MOTOR_Y_S1, HIGH);
  digitalWrite(MOTOR_Y_S2, HIGH);
  digitalWrite(MOTOR_Y_S3, HIGH);

  // read joystick values, ranges between [0,660]
  int V = analogRead(VERTICAL);
  int H = analogRead(HORIZONTAL);

  // map the joystick values linearly to the motor speed range
  int x_speed = map(H, JOYSTICK_MIN, JOYSTICK_MAX, -MOTOR_SPEED_MAX, MOTOR_SPEED_MAX);
  int y_speed = map(V, JOYSTICK_MIN, JOYSTICK_MAX, -MOTOR_SPEED_MAX, MOTOR_SPEED_MAX);
  
  // reject noise (or drift) in the joystick
  if (H >= JOYSTICK_MID_X - JOYSTICK_TOLERANCE && H <= JOYSTICK_MID_X + JOYSTICK_TOLERANCE) {
    x_speed = 0;
  }
  if (V >= JOYSTICK_MID_Y - JOYSTICK_TOLERANCE && V <= JOYSTICK_MID_Y + JOYSTICK_TOLERANCE) {
    y_speed = 0;
  }

  // speed scales with degree of joystick tilt
  stepperX.setSpeed(x_speed);
  stepperY.setSpeed(y_speed);

  stepperX.runSpeed();
  stepperY.runSpeed();
}
