constexpr size_t MAX_COLOR_BYTES = 63;
char colorBuffer[MAX_COLOR_BYTES + 1];
size_t colorLength = 0;
bool invalidColor = false;

void onColorReceived(const char* color) {
  Serial.println(color);
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 0) {
    const char value = Serial.read();
    if (value == '\n') {
      if (!invalidColor && colorLength > 0) {
        colorBuffer[colorLength] = '\0';
        onColorReceived(colorBuffer);
      }
      colorLength = 0;
      invalidColor = false;
    } else if (value == '\r' || value == '\0' || colorLength == MAX_COLOR_BYTES) {
      invalidColor = true;
    } else if (!invalidColor) {
      colorBuffer[colorLength++] = value;
    }
  }
}
