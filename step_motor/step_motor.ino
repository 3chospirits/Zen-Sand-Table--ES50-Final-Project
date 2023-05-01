#include <AccelStepper.h>
#define STEPS 200 // 250 steps is about 1mm   11.75cm per 25000 16th steps (0.47 mm / 16th step)
#define SOP '<' // beginning of transmission symbol

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

enum MODES { 
  Calibrate, // calibrate 0,0
  Drawing,
  Ready, // ready to recieve more instructions
  StartRecieving,
  Stop
};

const uint16_t VALS_PER_COORD = 4; // number of values stored for each x, y pair
const uint16_t BUFSIZE = 8 * VALS_PER_COORD; // store up to 50 coordinates in buffer

int16_t buf[BUFSIZE];
byte read_buf[BUFSIZE * 2];
int buffer_index = 0; // where we are in reading from the buffer
int buf_num = 0;
MODES mode = Ready;

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

  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  stepperX.setAcceleration(30000);
  stepperY.setAcceleration(30000);

  Serial.begin(9600);
  Serial.setTimeout(10000);

  mode = Ready; // CHANGE THIS for callibratioin
}

void loop() {
  digitalWrite(MOTOR1_S1, HIGH);
  digitalWrite(MOTOR1_S2, HIGH);
  digitalWrite(MOTOR1_S3, HIGH);

  digitalWrite(MOTOR2_S1, HIGH);
  digitalWrite(MOTOR2_S2, HIGH);
  digitalWrite(MOTOR2_S3, HIGH);

  /* DEBUG
  if (last_index != buffer_index){
    Serial.print("Buffer index");
    Serial.println(buffer_index);
    Serial.println(buffer_pos);
    last_index = buffer_index;
  }
  */
  
  // ready to ingest more data from Serial, and we are not full
  if (mode != Ready && buffer_index >= buffer_pos){
    buffer_pos = 0;
    buffer_index = 0;
    mode = Ready;
    Serial.println("ready");
  }

  if (mode == Ready) {
    while (mode != StartRecieving){
      while (!Serial.available());
      if ((char) Serial.read() == SOP) {mode = StartRecieving;}
    }

    while (!Serial.available());
    buffer_pos = Serial.readBytes(read_buf, BUFSIZE * 2);

    for (int i = 0; i < BUFSIZE * 2; i += 2) {
      int16_t val = (read_buf[i+1] << 8) | read_buf[i];
      buf[i / 2] = (read_buf[i+1] << 8) | read_buf[i]; // convert bytes to int
    }
    buf_num += 1;
    Serial.print("Buffer count: ");
    Serial.println(buf_num);
    
    mode = Drawing;
    buffer_index = 0;
  }
  
  if (mode == Drawing) {
    if (stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0){
      // get next instruction
      int x = buf[buffer_index];
      int y = buf[buffer_index + 1];
      int x_rpm = buf[buffer_index + 2];
      int y_rpm = buf[buffer_index + 3];
      buffer_index += 4;
      
      if (buffer_index * 100 / BUFSIZE % 10 == 0) {
        Serial.print("Motor progress: ");
        Serial.print(buffer_index * 100 / BUFSIZE);
        Serial.println("%");
      }
      
      stepperX.setMaxSpeed(x_rpm*10);
      stepperY.setMaxSpeed(y_rpm*10);
      stepperX.moveTo(stepperX.currentPosition() + x);
      stepperY.moveTo(stepperY.currentPosition() + y);
    }
  }
  stepperX.run();
  stepperY.run();
}
