int relayPin = 8;
int status;

void setup()
{
  pinMode(relayPin, OUTPUT);
  Serial.begin(9600);
}
void loop()
{ 
  Serial.print("Status:");
  if(Serial.available()){
    status = Serial.readStringUntil('\n').toInt(); 
    digitalWrite(relayPin, HIGH); 
    delay(1000);
  }
  
  else{
    digitalWrite(relayPin, LOW);
  }
   
}
