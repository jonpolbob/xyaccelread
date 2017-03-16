


void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
}


void loop() {
  // put your main code here, to run repeatedly:
int xvalue = analogRead(A0);
int yvalue = analogRead(A1);

unsigned char xbms = (unsigned char)(xvalue & 0x7F);
unsigned char ybms = (unsigned char)(yvalue & 0x7F);

unsigned char xbps = (unsigned char)(xvalue>>7) & 0x07;
unsigned char ybps = (unsigned char)(yvalue>>4) & 0x38;

Serial.write(xbps|ybps|0x80);// bps a 1
Serial.write(xbms);  // bps a 0
Serial.write(ybms); //bps a 0

delayMicroseconds(3000);

/*Serial.print(xbps|ybps|0x80);// bps a 1
Serial.print("::");

Serial.print(xbms);  // bps a 0
Serial.println(":");
Serial.print(ybms); //bps a 0
*/
/*Serial.print(xvalue); //bps a 0
Serial.print(":"); //bps a 0
Serial.print(yvalue); //bps a 0
Serial.println();
delay(500);
*/

}

