// Fill with the numbers for all the pins that read a potentiometer
int potPins[] = {A0, A1, A2, A3, A4};
int potCnt;

// Choose the BAUD rate for the serial connection (Recomended: 9600)
int baudRate = 9600;

void setup() {
  Serial.begin(baudRate);
  potCnt = sizeof(potPins)/sizeof(potPins[0]);
}

void loop() {
  if (sizeof(potPins) > 0){
    for(int i = 0; i < potCnt; i++){
      float sensorValue = (float)analogRead(potPins[i]);
      float out = sensorValue/1023.0;
      Serial.print(out);
      if (i < potCnt - 1){
        Serial.print("|");
      }
    }
  }
  Serial.println();

  delay(100);
}
