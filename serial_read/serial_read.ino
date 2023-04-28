const uint32_t BUFSIZE = 50 * 4; // store up to 50 coordinates in buffer
const uint32_t VALS_PER_COORD = 4;

int16_t buf[BUFSIZE];
int32_t ct = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (ct >= BUFSIZE) {
    for (int i = 0; i < BUFSIZE; i++){
      buf[i] = 0;
    }
    ct = 0;
    Serial.write(1); // tell python to send more coordinates
  }
  
  for (int i = 0; i < 4; i++){
    while (Serial.available() < 2){} // wait until there is data to read
    char read_buf[2];
    int bytes_read = Serial.readBytes(read_buf, 2);
    int16_t read_value = (uint8_t) read_buf[0] + ((uint8_t) read_buf[1] << 8);
    buf[ct + i] = read_value;
  }

  ct = ct + VALS_PER_COORD;
}
