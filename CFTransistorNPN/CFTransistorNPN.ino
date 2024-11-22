
/**************************
    www.usinainfo.com.br 
 **************************/
//Nodemcu ES8266 ESP32 = DO/GPIO16


const int chaveTactilPin = D0 ; 
  
void setup() {
  Serial.begin(9600); 
  pinMode(chaveTactilPin, OUTPUT); 
}
 
void loop() {
    Serial.println("--- desligou ---");

    digitalWrite(chaveTactilPin, LOW);
    delay(3000);

    Serial.println("--- ligou ---");

    digitalWrite(chaveTactilPin, HIGH);
    delay(3000);
}