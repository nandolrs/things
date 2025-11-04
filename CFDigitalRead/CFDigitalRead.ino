const int interruptorPino = A0; // nodemcu esp32 D1;
  
long duracao;
long leitura;

 
void setup() {
  Serial.begin(9600); 
  pinMode(interruptorPino, INPUT); 
}
 
// void loop() {
//   // Serial.print(".");

//   duracao = pulseIn(interruptorPino, LOW); // HIGH  LOW  , 60*1000
//   if (duracao > 0)
//   {
//     Serial.print("Duracao (ms): ");
//     Serial.println(duracao);
//   }
  
// }

// void loop() {
//   duracao = digitalRead(interruptorPino); 

//   Serial.print("Duracao (ms): ");
//   Serial.println(duracao);
  
//   delay(10);
// }

void loop() {
  leitura = analogRead(interruptorPino); 

  Serial.print("Leitura: ");
  Serial.println(leitura);
  delay(500);

}

// void loop1() {
//   duracao = digitalRead(interruptorPino); 

//   Serial.print("Duracao (ms): ");
//   Serial.println(duracao);
  
//   delay(1000);
// }



