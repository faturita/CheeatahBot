/* 
This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM
control

For use with the Adafruit Motor Shield v2 
---->  http://www.adafruit.com/products/1438
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
Adafruit_DCMotor *myMotor3 = AFMS.getMotor(3);
Adafruit_DCMotor *myMotor4 = AFMS.getMotor(4);
// You can also make another motor on port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  myMotor1->setSpeed(150);
  myMotor1->run(FORWARD);
  // turn on motor
  myMotor1->run(RELEASE);

  myMotor2->setSpeed(150);
  myMotor2->run(FORWARD);
  // turn on motor
  myMotor2->run(RELEASE);

  myMotor3->setSpeed(150);
  myMotor3->run(FORWARD);
  // turn on motor
  myMotor3->run(RELEASE);


  myMotor4->setSpeed(150);
  myMotor4->run(FORWARD);
  // turn on motor
  myMotor4->run(RELEASE);

}

void domotor(Adafruit_DCMotor *myMotor, int spd, int dir) {
  myMotor->setSpeed(spd);
  myMotor->run(dir);
}

void loop()
{
  domotor(myMotor3,255,FORWARD);
  domotor(myMotor4,255,FORWARD);
  
  int spd=0;
  for (spd=0;spd<255;spd++)
  {
    //domotor(myMotor1,spd,FORWARD);
    //domotor(myMotor2,spd,FORWARD);    
  }
  //domotor(myMotor3);
  //domotor(myMotor4);
  delay(1000);
  //domotor(myMotor1,0,RELEASE);
  //domotor(myMotor2,0,RELEASE);

  for (spd=0;spd<255;spd++)
  {
    //domotor(myMotor1,spd,BACKWARD);
    //domotor(myMotor2,spd,BACKWARD);
  }
  delay(1000);
  //domotor(myMotor1,0,RELEASE);
  //domotor(myMotor2,0,RELEASE);
}

