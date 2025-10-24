const int leituraPino = A0;// nodemcu esp-32 v3 = A0
const int ledPino = 5;// nodemcu esp-32 v3 = GPIO4 = D1

long leitura;
 
void setup() {
  Serial.begin(9600); 
  pinMode(leituraPino, INPUT); 
  pinMode(ledPino, OUTPUT); 

}
 

void loop() {
  leitura = analogRead(leituraPino); 

  Serial.print("leitura: ");
  Serial.println(leitura);

  digitalWrite(ledPino, HIGH);
  delay(1000);
  digitalWrite(ledPino, LOW);
  delay(1000);

}



