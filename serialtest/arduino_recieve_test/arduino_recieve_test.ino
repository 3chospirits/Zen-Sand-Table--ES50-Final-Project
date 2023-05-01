#define RX_PIN 0 // use the hardware serial port
#define TX_PIN 1 // use the hardware serial port
#define BUFFER_SIZE 50

typedef struct {
  int x;
  int y;
  int x_rpm;
  int y_rpm;
} Instruction;

Instruction buffer[BUFFER_SIZE];
int buffer_head = 0;
int buffer_tail = 0;
bool buffer_full = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Serial.println(Serial.available());
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    Serial.println(cmd);

    // if (cmd == "ready") {
    //   sendNextInstruction();
    // }
  }
}

void sendNextInstruction() {
  if (buffer_head == buffer_tail && !buffer_full) {
    return;
  }
  Instruction instr = buffer[buffer_tail];
  buffer_tail = (buffer_tail + 1) % BUFFER_SIZE;
  buffer_full = false;
  String msg = String(instr.x) + "," + String(instr.y) + "," + String(instr.x_rpm) + "," + String(instr.y_rpm) + "\n";
  Serial.print(msg);
}

void addToBuffer(int x, int y, int x_rpm, int y_rpm) {
  buffer[buffer_head] = {x, y, x_rpm, y_rpm};
  buffer_head = (buffer_head + 1) % BUFFER_SIZE;
  if (buffer_head == buffer_tail) {
    buffer_full = true;
  }
}
