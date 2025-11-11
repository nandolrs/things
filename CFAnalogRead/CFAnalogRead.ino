const int interruptorPino = A0; // nodemcu esp32 D1;
  
long duracao;
long leitura;


 
void setup() {
  Serial.begin(9600); 
  pinMode(interruptorPino, INPUT); 
}
 

void loop() {
  leitura = analogRead(interruptorPino); 

  Serial.print("Leitura analogica: ");
  Serial.println(leitura);
  delay(1000);

}







