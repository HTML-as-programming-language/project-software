// Fake Arduino client to simulate a client.
// Used to testing the Python backend code.

void setup()  
{
  Serial.begin(9600);
  while (!Serial) { }
}

void loop()
{
  Serial.write(0xff);
  Serial.write(0xff);

  Serial.write(0x00);
  Serial.write(0x65);

  Serial.write(0x00);
  Serial.write(0x00);

  /*Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
 
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
  Serial.write(0);
  
  
  Serial.write(0);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);
 
  Serial.write(1);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(1);
  Serial.write(0);*/

    delay(1000);
}

