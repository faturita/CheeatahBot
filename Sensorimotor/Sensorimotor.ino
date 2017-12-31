/**
    Basic Program to decode the driving signal of a DC Motor
    Particularly,

    DC Motor http://store.makeblock.com/optical-encoder-motor-25-6v-185rpm/

    Motor pins
     M+ M- GND VCC A B

     M+, M- Motor Power bidirectional
     GND, VCC .  Encoder power, 5V

     A - Digital Pin 2
     B - Digital Pin 4

     With this configuration it will work.  If you turn the motor
     you need to change the sign of the encoder counter on the
     Decoder function that is being callled at each interrupt.
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

bool debug = false;

class ControlledServo {
public:
  Servo servo;
  int pos;
  int tgtPos;
  int direction = 1;
  int minPos=0;
  int maxPos=180;

  void loop() {
      // Update desired position.
      if (pos<tgtPos)
        direction = 1;
      else
        direction =-1;  
  }

  void update() {

    loop();
    if (tgtPos != pos)
    {
      //Serial.print(pos);Serial.print("--");
      //Serial.println(tgtPos);
      servo.write(pos);
    
      pos+=direction;
      
      if (pos<minPos)
      {
        //Serial.print("Reset down:");
        //Serial.println(counter++);
        direction=-1;
      }
    
      if (pos>maxPos)
      {
        //Serial.print("Reset up:");
        //Serial.println(counter++);
        direction=1;    
      }
    }

  } 
};

ControlledServo scanner;
ControlledServo pan;

#define encoder1PinA  3
#define encoder1PinB  5

#define encoder2PinA  2
#define encoder2PinB  4


class MotorEncoder {
public:
  int encoderPinA;
  int encoderPinB;
  volatile long encoderPos = 0;
  long newposition;
  long oldposition = 0;
  unsigned long newtime;
  unsigned long oldtime = 0;
  long vel;  

  void setpins(int pencoder0PinA, int pencoder0PinB) 
  {
    encoderPinA = pencoder0PinA;
    encoderPinB = pencoder0PinB;  
  }

  void setup()
  {
    pinMode(encoderPinA, INPUT);
    digitalWrite(encoderPinA, HIGH);       // turn on pullup resistor
    pinMode(encoderPinB, INPUT);
    digitalWrite(encoderPinB, HIGH);       // turn on pullup resistor
  }

  void loop()
  {
    newposition = encoderPos;
    newtime = millis();
    int sign=1;
    if ((newposition - oldposition) < 0)
      sign = -1;
    vel = sign * (newposition - oldposition) * 1000 / (newtime - oldtime);
    vel = sign * encoderPos;
    //Serial.print (encoderPinA);
    //Serial.print (" speed = ");
    //Serial.println (vel);
    oldposition = newposition;
    oldtime = newtime;
  }

};

MotorEncoder motorencoder1;
MotorEncoder motorencoder2;

void doEncoder1()
{
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    motorencoder1.encoderPos--;
  } else {
    motorencoder1.encoderPos++;
  }
}

void doEncoder2()
{
  if (digitalRead(encoder2PinA) == digitalRead(encoder2PinA)) {
    motorencoder2.encoderPos++;
  } else {
    motorencoder2.encoderPos--;
  }
}



struct sensortype {
  int counter; // 2
  int armencoder; // 2
  long distance; // 4
  int16_t acx;    // 2
  int16_t acy;    // 2
  int16_t acz;    // 2
  int16_t temperature; // 2
  int16_t gx;    // 2
  int16_t gy;    // 2
  int16_t gz;    // 2
  long encoder1; // 4
  long encoder2; // 4
  int pan;        // 2
  int scan;       // 2
  int fps;        // 2
} sensor; // 36



// =========== DC Control using the encoder.
int targetpos = 0;
int TORQUE=255;

void setTargetPos(int newtargetpos)
{
  targetpos = newtargetpos;
}

bool updatedc(Adafruit_DCMotor *dcmotor, int currentpos)
{
  if (targetpos != currentpos)
  {
    dcmotor->setSpeed(TORQUE);

    if (targetpos < currentpos)
      dcmotor->run(BACKWARD);
    else
      dcmotor->run(FORWARD);

    return false;

  } else {
    dcmotor->setSpeed(0);
    return true;
  }

}



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

void setupencoder()
{
  motorencoder2.setpins(encoder2PinA, encoder2PinB);
  motorencoder2.setup();  
  attachInterrupt(digitalPinToInterrupt(encoder2PinA), doEncoder1, RISING);  // encoDER ON PIN 2

  motorencoder1.setpins(encoder1PinA, encoder1PinB);
  motorencoder1.setup();  
  attachInterrupt(digitalPinToInterrupt(encoder1PinA), doEncoder2, RISING);  // encoDER ON PIN 2  
}

void loopencoder()
{
  motorencoder1.loop();
  //motorencoder1.vel = motorencoder1.vel / 78.0;
  motorencoder2.loop();
  //motorencoder2.vel = motorencoder2.vel / 324.03;
  Serial.print( motorencoder1.vel  );
  Serial.print(' ');
  Serial.println(motorencoder2.vel ) ;
  delay(250);
}



void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("CheeatahBot Baby Monitor");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  // Set the speed to start, from 0 (off) to 255 (max speed)
  myMotor1->setSpeed(1);
  myMotor1->run(FORWARD);
  // turn on motor
  myMotor1->run(RELEASE);

  myMotor2->setSpeed(1);
  myMotor2->run(FORWARD);
  // turn on motor
  myMotor2->run(RELEASE);

  myMotor3->setSpeed(1);
  myMotor3->run(FORWARD);
  // turn on motor
  myMotor3->run(RELEASE);

 /**
    myMotor4->setSpeed(150);
    myMotor4->run(FORWARD);
    // turn on motor
    myMotor4->run(RELEASE);
  **/

  setupencoder();
  setupEncoder();
  setupUltraSensor();
  setupSuperSensor();

  scanner.servo.attach(10);
  scanner.pos=90;
  scanner.tgtPos=90; 

  pan.servo.attach(9);
  pan.pos = 57;
  pan.tgtPos = 57;// 57 is center

  setTargetPos(0);
  
}

void domotor(Adafruit_DCMotor *myMotor, int spd, int dir) {
  myMotor->setSpeed(spd);
  myMotor->run(dir);
}

void StateMachine(int state, int controlvalue)
{
  switch (state)
  {
    case 1:
      myMotor1->setSpeed(controlvalue);
      myMotor1->run(FORWARD);
      break;
    case 2:
      myMotor2->setSpeed(controlvalue);
      myMotor2->run(FORWARD);
      break;
    case 3:
      myMotor1->setSpeed(controlvalue);
      myMotor1->run(FORWARD);
      myMotor2->setSpeed(controlvalue);
      myMotor2->run(FORWARD); 
      break;  
    case 4:
      setTargetPos(controlvalue);
      break;   
    case 6:
      // Update desired position.
      pan.tgtPos = controlvalue;
      break;
    case 7:
      scanner.tgtPos = controlvalue;   
    default:
      // Do Nothing
      state = 0;
      break;

  }  
}

int speed=0;
int direction=1;

void loop()
{
  int state,controlvalue;
  
  sensor.fps = fps();

  parseCommand(state,controlvalue);
  
  updateEncoder();
  sensor.armencoder = getEncoderPos();
  
  //domotor(myMotor2, speed, FORWARD);
  //domotor(myMotor1, speed, FORWARD);
  updatedc(myMotor3, getEncoderPos());

  speed = speed + direction*1;

  if (speed>120)
    direction=-1;

  if (speed<=5)
    direction=1;

  /**
    int spd=0;
    for (spd=0;spd<255;spd++)
    {
    domotor(myMotor1,spd,FORWARD);
    domotor(myMotor2,spd,FORWARD);
    }

    delay(1000);
    domotor(myMotor1,0,RELEASE);
    domotor(myMotor2,0,RELEASE);

    for (spd=0;spd<255;spd++)
    {
    domotor(myMotor1,spd,BACKWARD);
    domotor(myMotor2,spd,BACKWARD);
    }
    delay(1000);
    domotor(myMotor1,0,RELEASE);
    domotor(myMotor2,0,RELEASE);**/

  //loopencoder();

  checksensors();
  //updateUltraSensor();
  updateSuperSensor();

  pan.update();
  sensor.pan = pan.pos;
  scanner.update();
  sensor.scan = scanner.pos;

  StateMachine(state,controlvalue);
}






