const int interruptorPino = A0;// nodemcu esp-32 v3 = A0
  
long duracao;
 
void setup() {
  Serial.begin(9600); 
  pinMode(interruptorPino, INPUT); 
}
 
void loop1() {
  duracao = pulseIn(interruptorPino, LOW, 60*1000); // HIGH
  if (duracao > 0)
  {
    Serial.print("Duracao (ms): ");
    Serial.println(duracao);
  }
  
  delay(1000);
}

void loop() {
  duracao = analogRead(interruptorPino); 

  Serial.print("Duracao (ms): ");
  Serial.println(duracao);
  
  delay(1000);
}



