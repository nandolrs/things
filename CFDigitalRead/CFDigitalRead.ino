const int interruptorPino = A0; // nodemcu esp32 D1;
  
long duracao;
long leitura;

 
void setup() {
  Serial.begin(9600); 
  pinMode(interruptorPino, INPUT); 
}
 

void loop() {
  leitura = digitalRead(interruptorPino); 

  Serial.print("Leitura digital: ");
  Serial.println(leitura);
  delay(500);

}


