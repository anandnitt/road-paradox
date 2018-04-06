void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(8,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

char x=Serial.read();
if(x=='a')
digitalWrite(8,LOW);
else
digitalWrite(8,HIGH);
delay(1000);
}
