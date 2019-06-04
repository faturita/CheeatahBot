
/**
 * The ultrasound sensor works with only one SIG pin (instead of trig and echo)
 * 
 */


void setupUltraSensor() {
  // put your setup code here, to run once:
  //Serial.begin (9600);
  //pinMode(trigPin, OUTPUT);
  //pinMode(echoPin, INPUT);
  //pinMode(led, OUTPUT);
  //pinMode(led2, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}


inline void  updateUltraSensor() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;


  if (distance < 4) {  // This is where the LED On/Off happens
    //digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off
    //digitalWrite(led2,LOW);
  }
  else {
    //digitalWrite(led,LOW);
    //digitalWrite(led2,HIGH);
    if (debug) Serial.print(distance);
    if (debug) Serial.println(" cm");
  }
  
  if (distance >= 200 || distance <= 0){
    if (debug) Serial.println("Out of range");
  }
  else {
    //if (debug) Serial.print(distance); 
    //if (debug) Serial.println(" cm");
  }
  sensor.distance = distance;

  //delay(10);
}
