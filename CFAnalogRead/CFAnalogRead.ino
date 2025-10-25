const int leituraPino = A0;// nodemcu esp-32 v3 = A0
const int ledPino = 5;// nodemcu esp-32 v3 = GPIO5 = D1
const int ledCondicaoPino = 2;// nodemcu esp-32 v3 = GPIO4 = D4

long leitura;
const int limiteCondicao = 1; //  
 
void setup() {
  Serial.begin(9600); 
  pinMode(leituraPino, INPUT); 
  pinMode(ledPino, OUTPUT); 
  pinMode(ledCondicaoPino, OUTPUT); 

}
 

void loop() {
  leitura = analogRead(leituraPino); 

  Serial.print("leitura: ");
  Serial.println(leitura);

  digitalWrite(ledPino, HIGH);
  if (leitura > limiteCondicao)
  {
    digitalWrite(ledCondicaoPino, HIGH);
  }  
  delay(1000);
  digitalWrite(ledPino, LOW);
  digitalWrite(ledCondicaoPino, LOW);
  delay(1000);

}



