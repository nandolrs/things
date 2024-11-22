
/**************************
    www.usinainfo.com.br 
 **************************/
 
const int echoPin =D5 ;// D5; 20;05; 1
const int trigPin =D6 ;//D6 ;19;04; 2
 
//define sound speed in cm/uS
#define SOUND_SPEED 0.0343D
#define CM_TO_INCH 0.393701D
 
long duration;
float distanceCm;
float distanceInch;
 
void setup() {
  Serial.begin(9600); 
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
}
 
void loop() {
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); // 10
  digitalWrite(trigPin, LOW);
  
 
  duration = pulseIn(echoPin, HIGH);
  
  distanceCm = duration;// * SOUND_SPEED/2;
  
  Serial.print("Distancia (cm): ");
  Serial.println(distanceCm);
  
  delay(1000);
}