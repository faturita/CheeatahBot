int incomingByte = 0;

char buffer[5];

void readcommand(int &state, int &controlvalue)
{
  // Format ACNNN, 'A', C is command, NNN is the controlvalue.
  memset(buffer, 0, 5);
    int readbytes = Serial.readBytes(buffer, 4);
    
    if (readbytes == 4) {
      if (debug) Serial.println ( (int)buffer[0] );
      int action = 0;
      if ((buffer[0] == 'B') || (buffer[0] == 'C') || (buffer[0] == 'D') || (buffer[0] == 'E'))  // send alpha hexa actions.
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
    int action;

    switch (syncbyte) 
    {
      case 'I':
        Serial.println("CHET");
        break;
      case 'V':
        Serial.println(codeversion);
        break;
      case 'S':
        startburst();
        break;
      case 'R':
        resetEncoders();
        break;
      case '%':
        precise = !precise;
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
        updateSuperSensor();
        Serial.print(sensor.acx);Serial.print(":");Serial.print(sensor.acy);Serial.print(",");Serial.print(sensor.acz);Serial.print(",");Serial.print(sensor.distance);Serial.println();
        break;
      case 'K':
        updateUltraSensor();
        break;
      case '=':
        homing = 1;
        homingcounter=0;
        //setTargetPos(200-150);
        //resetEncoderPos();
        //setTargetPos(0);
        state=0;
        //setTargetPos(90/10);
        //elbow.tgtPos=90;
        //wrist.tgtPos=90;
        //homing=true;
        break;
      case 'A':
        readcommand(action,controlvalue);
        switch(action)
        {
          case 0x0b:
            setBurstSize(controlvalue);
            state = 0;
            break;
          case 0x0c:
            payloadsize();
            state = 0;
            break;
          case 0x0d:
            payloadstruct();
            state = 0;
            break;
          case 0x0e:
            setUpdateFreq(controlvalue);
            state = 0;
            break;
          default:
            state = action;
            break;
        }
        break;
      case 'O':
        setDoScan();
        break;
      default:
        break;
    }

  }

}

