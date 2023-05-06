// step_motor.ino
// Script intercepts instructions from serial port in the form of (delta_x, delta_y, rpm_x, rpm_y)
// and moves each motor accordingly.

// TODO: CHECK UPDATED CODE
#include <AccelStepper.h>
#define SOP '<' // beginning of transmission symbol

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

// stepper motors
AccelStepper stepperX(AccelStepper::DRIVER, MOTOR_XA, MOTOR_XB);
AccelStepper stepperY(AccelStepper::DRIVER, MOTOR_YA, MOTOR_YB);

enum MODES { 
  DRAWING,                  // currently draining queue and drawing
  READY_FOR_INSTRUCTIONS,   // ready to recieve more instructions
  START_RECIEVING           // have recieved SOP, ready to add instructions to buffer
};

const uint16_t VALS_PER_COORD = 4;            // number of values stored for each x, y pair
const uint16_t BUFSIZE = 8 * VALS_PER_COORD;  // store up to 8 instructions in buffer/queue

int16_t buf[BUFSIZE];       // buffer for storing instructions
byte read_buf[BUFSIZE * 2]; // temp buffer for reading from serial
int buffer_index = 0;       // index of next instruction to be executed
int buf_num = 0;

MODES mode = READY_FOR_INSTRUCTIONS;

void setup() {
  // setup pin modes
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

  Serial.begin(9600);
  Serial.setTimeout(10000);

  mode = READY_FOR_INSTRUCTIONS;
}

void loop() {
  // set both motor drivers to sixteenth-step resolution (max precision)
  digitalWrite(MOTOR_X_S1, HIGH);
  digitalWrite(MOTOR_X_S2, HIGH);
  digitalWrite(MOTOR_X_S3, HIGH);

  digitalWrite(MOTOR_Y_S1, HIGH);
  digitalWrite(MOTOR_Y_S2, HIGH);
  digitalWrite(MOTOR_Y_S3, HIGH);

  // ready to ingest more data from Serial, and we are not full
  if (mode != READY_FOR_INSTRUCTIONS && buffer_index >= BUFSIZE){
    buffer_index = 0;
    mode = READY_FOR_INSTRUCTIONS;
    Serial.println("ready");
  }

  // wait for SOP then set mode into receiving
  if (mode == READY_FOR_INSTRUCTIONS) {
    while (mode != START_RECIEVING){
      while (!Serial.available());
      if ((char) Serial.read() == SOP) {mode = START_RECIEVING;}
    }

    while (!Serial.available());

    // copy bytes from serial into read_buf
    Serial.readBytes(read_buf, BUFSIZE * 2);

    // convert bytes to int
    for (int i = 0; i < BUFSIZE * 2; i += 2) {
      buf[i / 2] = (read_buf[i+1] << 8) | read_buf[i]; 
    }
    buf_num += 1;
    Serial.print("Buffer count: ");
    Serial.println(buf_num);
    
    // finish reading instructions
    mode = DRAWING;
    buffer_index = 0;
  }
  
  if (mode == DRAWING) {
    if (stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0){
      // get next instruction
      int x = buf[buffer_index];
      int y = buf[buffer_index + 1];
      int x_rpm = buf[buffer_index + 2];
      int y_rpm = buf[buffer_index + 3];
      buffer_index += 4;
      
      // print motor progress
      if (buffer_index * 100 / BUFSIZE % 10 == 0) {
        Serial.print("Motor progress: ");
        Serial.print(buffer_index * 100 / BUFSIZE);
        Serial.println("%");
      }
      
      // input instructions to motors
      stepperX.setMaxSpeed(x_rpm * 10);
      stepperY.setMaxSpeed(y_rpm * 10);
      stepperX.moveTo(stepperX.currentPosition() + x);
      stepperY.moveTo(stepperY.currentPosition() + y);
    }
  }
  stepperX.run();
  stepperY.run();
}
