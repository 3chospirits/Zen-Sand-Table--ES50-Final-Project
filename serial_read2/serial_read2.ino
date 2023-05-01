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
  // reset buffer
  for (int i = 0; i < BUFSIZE; i++){
    buf[i] = 0x00;
  }
  buffer_pos = 0; // reset buffer position
  
  //Serial.println(buf_num);

  Serial.write(buf_num); // tell python to send more data

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
    while(true); // stop execution if there was a communication error
  }

  for (int i = 0; i < BUFSIZE * 2; i += 2) {
    buf[i / 2] = (read_buf[i+1] << 8) | read_buf[i]; // convert bytes to int
  }
  
  buffer_pos = BUFSIZE;
  buf_num = buf_num + 1; // increment count of buffers filled
}
