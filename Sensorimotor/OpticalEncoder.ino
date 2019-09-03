// Pins for the optical encoder inputs.
// The pin 2 and 3 are the interrupt pins 0 and 1 for Arduino UNO
#define RH_ENCODER_A 3 
#define RH_ENCODER_B 5
#define LH_ENCODER_A 2
#define LH_ENCODER_B 4

// variables to store the number of encoder pulses
// for each motor
// volatile is used to indicate not to use cpu register and instead, use memory locations.
volatile  long leftCount = 0;
volatile  long rightCount = 0;


// encoder event for the interrupt call
// In a differential wheel configuration, one motor should increase the counter (moving forward) while the other, for the same pin level, should
// decrease it (motor axis are opposed).
void leftEncoderEvent() {
  if (digitalRead(LH_ENCODER_A) == HIGH) {
    if (digitalRead(LH_ENCODER_B) == LOW) {
      leftCount++;
    } else {
      leftCount--;
    }
  } else {
    if (digitalRead(LH_ENCODER_B) == LOW) {
      leftCount--;
    } else {
      leftCount++;
    }
  }
}

// encoder event for the interrupt call
void rightEncoderEvent() {
  if (digitalRead(RH_ENCODER_A) == HIGH) {
    if (digitalRead(RH_ENCODER_B) == LOW) {
      rightCount--;
    } else {
      rightCount++;
    }
  } else {
    if (digitalRead(RH_ENCODER_B) == LOW) {
      rightCount++;
    } else {
      rightCount--;
    }
  }
}

void setupMotorEncoders()
{
  pinMode(LH_ENCODER_A, INPUT);
  pinMode(LH_ENCODER_B, INPUT);
  pinMode(RH_ENCODER_A, INPUT);
  pinMode(RH_ENCODER_B, INPUT);
  
  // initialize hardware interrupts
  attachInterrupt(digitalPinToInterrupt(LH_ENCODER_A), leftEncoderEvent, CHANGE);
  attachInterrupt(digitalPinToInterrupt(RH_ENCODER_A), rightEncoderEvent, CHANGE);  
}

void loopEncoders()
{
  sensor.rightEncoder = rightCount;
  sensor.leftEncoder = leftCount;  

  if (debug)
  {
    Serial.print("L:");Serial.print(leftCount);Serial.print("-R:");Serial.println(rightCount);
  }
}

void resetEncoders()
{
  rightCount = 0; 
  leftCount = 0;
  
}

