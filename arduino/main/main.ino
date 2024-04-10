void setup() {
  Serial.begin(9600);
}

void loop() {
  float sensorValue = (float)analogRead(A0);
  float out = sensorValue/1023.0;
  Serial.print(out);
  for(int i=0; i<10; i++){
    Serial.print("|");
    Serial.print(out);
  }
  Serial.println();

  delay(100);
}
