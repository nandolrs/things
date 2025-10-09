const int interruptorPino = D1; // nodemcu esp32 D1;
  
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
  duracao = digitalRead(interruptorPino); 

  Serial.print("Duracao (ms): ");
  Serial.println(duracao);
  
  delay(1000);
}



