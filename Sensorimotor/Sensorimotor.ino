/**
    CheatahBot

     Tilt sensor
     G - GND
     R - VCC
     Y - Signal - 8

*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

unsigned long tick = 0;
bool debug = false;
char* codeversion="1.0";

bool precise = false;

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

struct sensortype {
  float fps;     // 4
  long rightEncoder; // 4
  long leftEncoder; // 4 
  long distance; // 4 
  int counter; // 2
  int armencoder; // 2
  int16_t acx;    // 2
  int16_t acy;    // 2
  int16_t acz;    // 2
  int16_t temperature; // 2
  int16_t gx;    // 2
  int16_t gy;    // 2
  int16_t gz;    // 2
  int pan;        // 2
  int scan;       // 2
  int freq;        // 2
} sensor; // 40



// =========== DC Control using the encoder.
int targetpos = 0;
int TORQUE=1;

int oldcurrentpos=0;

void setTargetPos(int newtargetpos)
{

  targetpos = newtargetpos;
  TORQUE=1;

}

int increaseTorque()
{
  if ((TORQUE++)<=255)
    TORQUE=255;
  return TORQUE;
}

bool updatedc(Adafruit_DCMotor *dcmotor, int currentpos)
{ 
  int torq=0;

  if (targetpos < currentpos) torq=130;
  if (targetpos > currentpos) torq=50;
  
  if (targetpos != currentpos)
  {
    dcmotor->setSpeed(torq);

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



bool pcontrol(Adafruit_DCMotor *dcmotor, int torq, int targetpos, int currentpos)
{ 
  int error = 40;

  if ((targetpos<(currentpos-error))||(targetpos>(currentpos+error)))
  {
    dcmotor->setSpeed(torq);

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
Adafruit_DCMotor *rightMotor = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(2);
Adafruit_DCMotor *elbowMotor = AFMS.getMotor(3);
Adafruit_DCMotor *myMotor4 = AFMS.getMotor(4);
// You can also make another motor on port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void domotor(Adafruit_DCMotor *myMotor, int spd, int dir) {
  myMotor->setSpeed(spd);
  myMotor->run(dir);
}

const int TILT_PIN = 8;

bool checktilted()
{
  int tiltVal = digitalRead(TILT_PIN);
  if (tiltVal == HIGH) {
    return true;
  } else {
    return false;
  }
}

// Scanner =======

bool doscan = false;
int scanstate = 0;
int scancounter=0;
int scanvalues[4];

void setDoScan()
{
  doscan = !doscan;  
}

void scan()
{
  if (doscan)
  {
    if (scancounter>500)
    {
      if (sensor.fps > 30)
      {
        updateUltraSensor();
        scanvalues[scanstate] = sensor.distance;
      } 
    }
    if (scancounter++>1000)
    {
      switch (scanstate)
      {
        case 0:
          scanner.tgtPos = 30;
          scanstate=1;
          scancounter=0;
          break;
        case 1:
          scanner.tgtPos = 90;
          scanstate=2;
          scancounter=0;
          break;
        case 2:
          scanner.tgtPos = 160;
          scanstate=3;
          scancounter=0;
          break;
        case 3:
          scanner.tgtPos = 90;
          scanstate=0;
          scancounter=0;
          break;
        default:
          scanstate=0;
          scancounter=0;
      }     
    }
  }
  
}

int StateMachine(int state, int controlvalue)
{
  static int previousState = 0;
  switch (state)
  {
    case 1:
      // Left
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(FORWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(BACKWARD); 
      break;
    case 2:
      // Right
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(BACKWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(FORWARD);
      break;
    case 3:
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(FORWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(FORWARD); 
      break; 
    case 4:
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(BACKWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(BACKWARD); 
      break;   
    case 5:
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(BACKWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(FORWARD); 
      break;  
    case 6:
      rightMotor->setSpeed(controlvalue);
      rightMotor->run(FORWARD);
      leftMotor->setSpeed(controlvalue);
      leftMotor->run(BACKWARD); 
      break;  
    case 7:
      setTargetPos(controlvalue-150);
      break;   
    case 8:
      // Update desired position.
      pan.tgtPos = controlvalue;
      break;
    case 9:
      scanner.tgtPos = controlvalue;  
      break;
    case 0x0a:
      rightMotor->run(RELEASE);
      leftMotor->run(RELEASE);
      elbowMotor->run(RELEASE);
      resetEncoderPos();
      targetpos=0; 
      break;
    default:
      // Do Nothing
      resetEncoders();
      state = 0;
      break;
  }  
  previousState = state;
  return state;
}


int homingcounter=0;
int homing=0;

void doHome()
{
  if (homing>0)
    homingcounter++;
    
  switch(homing)
  {
    case 0:
      break;
    case 1:
      if (homingcounter>120)
      {
        setTargetPos(200-150);
        homing=2;       
      }
      break;
     case 2:
      if (homingcounter>450)
      {
        resetEncoderPos();
        setTargetPos(10-150);
        homing=3;
      }
      break;
     case 3:
      if (homingcounter>490)
      {
        if (!checktilted())
        {
          resetEncoderPos();
          setTargetPos(0);
          homingcounter=0;
          homing=0;
        }        
      }
      break;
    default:
      break;
  }
}

#define trigPin 6
#define echoPin 7

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.setTimeout(1000);      // timeout in milliseconds
  Serial.print("CheeatahBot v");Serial.println(codeversion);

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  // Set the speed to start, from 0 (off) to 255 (max speed)
  rightMotor->setSpeed(1);
  rightMotor->run(FORWARD);
  // turn on motor
  rightMotor->run(RELEASE);

  leftMotor->setSpeed(1);
  leftMotor->run(FORWARD);
  // turn on motor
  leftMotor->run(RELEASE);

  elbowMotor->setSpeed(1);
  elbowMotor->run(FORWARD);
  // turn on motor
  elbowMotor->run(RELEASE);

  setupMotorEncoders();
  setupEncoder();
  //setupUltraSensor();
  setupSuperSensor();

  scanner.servo.attach(10);
  scanner.pos=0;
  scanner.tgtPos=90; 

  pan.servo.attach(9);
  pan.pos = 0;
  pan.tgtPos = 60;// 57 is center

  setTargetPos(0);

  
  pinMode(TILT_PIN, INPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

unsigned long previousMillis = 0;        // will store last time LED was updated

// duration of movement.
long interval = 2000;           // interval of duration of movement


void loop()
{
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
    //if (debug) Serial.print(distance);
    //if (debug) Serial.println(" cm");
  }
  
  if (distance >= 200 || distance <= 0){
    //if (debug) Serial.println("Out of range");
  }
  else {
    //if (debug) Serial.print(distance); 
    //if (debug) Serial.println(" cm");
  }
  sensor.distance = distance;
  
  int state,controlvalue;
  unsigned long currentMillis = millis();
  
  sensor.freq = freq();
  sensor.fps = 0.0;

  parseCommand(state,controlvalue);
  
  updateEncoder();
  sensor.armencoder = getEncoderPos();
  
  updatedc(elbowMotor, getEncoderPos());


  loopEncoders();
//  if (currentMillis - previousMillis >= interval) {
//    // save the last time you blinked the LED
//    previousMillis = currentMillis;
//
//    Serial.println( scancounter );
//    Serial.println( state );
//
//    if (state != 0)
//    {
//      Serial.println("STop");
//      scancounter=1;
//      setDoScan();
//    } else if (scancounter>0) {
//      if (scanvalues[1] > scanvalues[0] && scanvalues[1] > scanvalues[3])
//        {
//          Serial.println("LEft");
//        }
//    
//    
//      if (scanvalues[3] > scanvalues[0] && scanvalues[3] > scanvalues[1])
//        {
//          Serial.println("Right");
//        }
//
//      if (scanvalues[0] > scanvalues[1] && scanvalues[0] > scanvalues[3])
//        {
//          Serial.println("Ahead");
//        }
//    }
//  }

  //updateUltraSensor();
  if (checksensors())
  {
    updateSuperSensor();
  }
  burstsensors();

  scan();
  doHome();

  pan.update();
  sensor.pan = pan.pos;
  scanner.update();
  sensor.scan = scanner.pos;

  StateMachine(state,controlvalue);

  //delay(250);
}




