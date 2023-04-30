#define SOP '<'
#define EOP '>'

const uint16_t VALS_PER_COORD = 4; // number of values stored for each x, y pair
const uint16_t BUFSIZE = 50 * VALS_PER_COORD; // store up to 50 coordinates in buffer

int16_t buf[BUFSIZE];
byte read_buf[BUFSIZE * 2];
int16_t buffer_pos = 0;
int16_t buf_num = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (buffer_pos >= BUFSIZE) {
    // reset buffer
    for (int i = 0; i < BUFSIZE; i++){
      buf[i] = 0x00;
    }
    buffer_pos = 0; // reset buffer position
    buf_num = buf_num + 1; // increase count of buffers filled

    Serial.write((byte) buf_num); // tell python to send more data
  }

  // wait for start marker
  bool start_marker_received = false;
  while(!start_marker_received) {
    while(!Serial.available());
    char read_char = Serial.read();
    start_marker_received = (read_char == SOP);
  }

  while(!Serial.available());
  int16_t bytes_read = Serial.readBytesUntil(EOP, read_buf, BUFSIZE * 2);
  if (bytes_read != BUFSIZE * 2) {
    // Serial.print("WRONG NUMBER BYTES READ");
  }

  for (int i = 0; i < BUFSIZE * 2; i += 2) {
    buf[i / 2] = (read_buf[i+1] << 8) | read_buf[i]; // convert bytes to int
  }
  buffer_pos = BUFSIZE;
  
  //for (int i = 0; i < 4; i++){   
    //while (Serial.available() < 2){} // wait until there is data to read
    //byte temp_buf[2];
    //int16_t bytes_read = Serial.readBytes(temp_buf, 2);
    //int16_t read_value = (temp_buf[1] << 8) | temp_buf[0]; // convert bytes to int
    //buf[buffer_pos] = read_value;
    //buffer_pos = buffer_pos + 1;
  //}
}
