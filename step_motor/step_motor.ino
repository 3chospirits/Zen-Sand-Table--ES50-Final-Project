#include <AccelStepper.h>
#define STEPS 200 // 250 steps is about 1mm   11.75cm per 25000 16th steps (0.47 mm / 16th step)
#define MOTOR_SPEED 500
#define QUEUE_SIZE 10
#define SOP '<'
#define EOP '>'

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

const uint16_t VALS_PER_COORD = 4; // number of values stored for each x, y pair
const uint16_t BUFSIZE = 50 * VALS_PER_COORD; // store up to 50 coordinates in buffer

int16_t buf[BUFSIZE];
byte read_buf[BUFSIZE * 2];
int buffer_pos = 0;   // "length" buffer
int buffer_index = 0; // where we are in reading from the buffer

enum MODES { 
  Callibrate, // callibrate 0,0
  Drawing,
  Ready, // ready to recieve more instructions
  StartRecieving,
  Stop
};
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

int last_index = 0;
void loop() {
  digitalWrite(MOTOR1_S1, HIGH);
  digitalWrite(MOTOR1_S2, HIGH);
  digitalWrite(MOTOR1_S3, HIGH);

  digitalWrite(MOTOR2_S1, HIGH);
  digitalWrite(MOTOR2_S2, HIGH);
  digitalWrite(MOTOR2_S3, HIGH);

  if (last_index != buffer_index){
    Serial.print("Buffer index");
    Serial.println(buffer_index);
    Serial.println(buffer_pos);
    last_index = buffer_index;
  }
  // ready to ingest more data from Serial, and we are not full
  if (mode != Ready && buffer_index >= buffer_pos){
    buffer_pos = 0;

    mode = Ready;
    Serial.println("ready");
  }

  if (mode == Ready) {
    while (mode != StartRecieving){
      while (!Serial.available());
      char read_char = Serial.read();
      if (read_char == SOP) mode = StartRecieving;
    }

    while (!Serial.available());
    buffer_pos = Serial.readBytesUntil(EOP, read_buf, BUFSIZE * 2);

    for (int i = 0; i < BUFSIZE * 2; i += 2) {
      buf[i / 2] = (read_buf[i+1] << 8) | read_buf[i]; // convert bytes to int
    }
//    buffer_pos = BUFSIZE;
    mode = Drawing;
  }
  if (mode == Drawing) {
    if (stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0){
      // get next instruction
      int x = buf[buffer_index];
      int y = buf[buffer_index + 1];
      int x_rpm = buf[buffer_index + 2];
      int y_rpm = buf[buffer_index + 3];
      buffer_index += 4;
      Serial.print("Running instructions: ");
      Serial.print(x);
      Serial.print(" ");
      Serial.print(y); 
      Serial.print(" ");
      Serial.print(x_rpm); 
      Serial.print(" ");
      Serial.println(y_rpm); 
      stepperX.setMaxSpeed(x_rpm*10);
      stepperY.setMaxSpeed(y_rpm*10);
      stepperX.moveTo(stepperX.currentPosition() + x);
      stepperY.moveTo(stepperY.currentPosition() + y);
    }
  }
  stepperX.run();
  stepperY.run();
}

// void loop() {
//   // if there is instructions in the buffer

//   if (ct >= BUFSIZE) {
//     for (int i = 0; i < BUFSIZE; i++){
//       buf[i] = 0;
//     }
//     ct = 0;
//     Serial.write(1); // tell python to send more coordinates
//   }
  
//   for (int i = 0; i < 4; i++){
//     while (Serial.available() < 2){} // wait until there is data to read
//     char read_buf[2];
//     int bytes_read = Serial.readBytes(read_buf, 2);
//     int16_t read_value = (uint8_t) read_buf[0] + ((uint8_t) read_buf[1] << 8);
//     Serial.println(read_value);
//     buf[ct + i] = read_value;
//   }
//   ct = ct + VALS_PER_COORD;
// }