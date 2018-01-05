int incomingByte = 0;

char buffer[5];

void readcommand(int &state, int &controlvalue)
{
  // Format A1000 >> A1220   --> Close grip
  // A2255 >> Open Grip
  // A6090 >> 90 deg wrist A6010 --> A6180
  // A3220 or A4220 Move forward backward shoulder NO LONGER
  // A7150 will keep the shoulder at zero encoder angle arm vertical. 
  //       So AA140 will pull it up
  // A8220 clockwise A9220 counter
  // AA180 -> Elbow is now a degree based encoder.  Not rotational.
  // Format A5000  Reset everything.
  memset(buffer, 0, 5);
  int readbytes = Serial.readBytes(buffer, 4);

  if (readbytes == 4) {
    if (debug) Serial.println ( (int)buffer[0] );
    int action = 0;
    if (buffer[0] >= 65)  // send alpha hexa actions.
      action = buffer[0] - 65 + 10;
    else
      action = buffer[0] - 48;
    int a = buffer[1] - 48;
    int b = buffer[2] - 48;
    int c = buffer[3] - 48;

    controlvalue = atoi(buffer + 1);
    state = action;

    if (debug) {
      Serial.print("Action:");
      Serial.print(action);
      Serial.print("/");
      Serial.println(controlvalue);
    }
  }
}

void parseCommand(int &state, int &controlvalue)
{
  if (Serial.available() > 0) 
  {

    char syncbyte = Serial.read();

    switch (syncbyte) 
    {
      case 'I':
        Serial.println("CHET");
        break;
      case 'S':
        startburst();
        break;
      case 'X':
        stopburst();
        break;
      case 'D':
        debug = (!debug);
        break;
      case 'L':
        //digitalWrite(laserPin, HIGH);
        break;
      case 'l':
        //digitalWrite(laserPin, LOW);
        break;
      case 'Q':
        Serial.println( sensor.armencoder );
        break;
      case 'U':
        Serial.print(sensor.acx);Serial.print(":");Serial.print(sensor.acy);Serial.print(",");Serial.print(sensor.acz);Serial.print(",");Serial.println();
        break;
      case '=':
        resetEncoderPos();
        //targetpos=0;
        //setTargetPos(90/10);
        //elbow.tgtPos=90;
        //wrist.tgtPos=90;
        //homing=true;
        break;
      case 'A':
        readcommand(state,controlvalue);
        break;
      default:
        break;
    }

  }

}

