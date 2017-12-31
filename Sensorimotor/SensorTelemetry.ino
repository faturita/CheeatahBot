#define MAX_SIZE_SENSOR_BURST 100

int fps()
{
  static int freqValue = 200;
  static int freqCounter = 0;
  static unsigned long myPreviousMillis = millis();
  unsigned long myCurrentMillis = 0;

  myCurrentMillis = millis();

  if ((myCurrentMillis - myPreviousMillis) > 1000)
  {
    if (debug)
    {
      Serial.print("Frequency:"); Serial.println(freqCounter);
    }
    myPreviousMillis = myCurrentMillis;
    freqValue = freqCounter;
    freqCounter = 0;
  }
  else
  {
    freqCounter++;
  }
  return freqValue;
}


void checksensors()
{
  static int counter = 0;
  if (counter >= 255)
  {
    counter = 0;
  }
  sensor.counter = counter++;

}

bool sensorburst = false;
int sampleCounter = 0;

void burstsensors() {
  if (sensorburst)
  {
    transmitsensors();
    sampleCounter++;
    if (sampleCounter > MAX_SIZE_SENSOR_BURST)
    {
      sensorburst = false;
      sampleCounter = 0;
    }
  }
}

void startburst()
{
  sensorburst = true;
  // Reset counter to avoid loosing data.
  sampleCounter = 0;
}

void stopburst()
{
  sensorburst = false;  
}

void transmitsensors() {
  int len = sizeof(sensor);
  char aux[len];  //36
  memcpy(&aux, &sensor, len);

  Serial.write('S');
  Serial.write((uint8_t *)&aux, len);
  Serial.write('E');

  if (debug) {
    Serial.println('S');
    Serial.print("Cx:"); Serial.println(sensor.acx);
    Serial.print("Cy:"); Serial.println(sensor.acy);
    Serial.print("Cz:"); Serial.println(sensor.acz);
    Serial.print("Encoder:"); Serial.println(sensor.armencoder);
    Serial.println(']');
  }


  //Aguarda 5 segundos e reinicia o processo
  //delay(5000);
}


