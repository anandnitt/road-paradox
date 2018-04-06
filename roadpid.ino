#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>



#include <math.h>
#include <arduino.h>
volatile float Time_period;
int count,r=0;
float Set_rpm = 0;
float Previous_error = 0;
float D_error = 0;
float I_error = 0;
float P_gain = 0.9;
float I_gain = 0.005;
float D_gain = 0.3;
float Dt = 0.5;
float Error;
int Required_rpm=0;///TARGET__RPM
float Final      =255;///INITIAL__PWM(333-RPM)
int Present_rpm;
float H;
float I;
float P;
float D;
float Total_error;
float k;
int Acc;
int mode=0;
char x;
int main ()
{
    EICRA|=(1<<ISC00)|(1<<ISC01);
    EIMSK|=(1<<INT0); 
    TCCR0A=(1<<WGM00)|(1<<COM0B1)|(1<<COM0A1);
    TCCR0B=(1<<CS02);
    sei();
    DDRD = 0b01100000;   
    Serial.begin(9600);
   int Acc= 200;
   int a=100;
    while (1) 
    {   
      while(UCSR0A!= (UCSR0A|(1<<RXC0)));
   x=UDR0;
       Required_rpm=x;
       OCR0A=Final;
      OCR0B=Final;
     }
 }


void Timer1_init()
{
  TCCR1B|=(1<<CS12)|(1<<CS10);
  TCNT1=0;
}



ISR(INT0_vect)
{
  count++;
  if(count==1)
  {
    Timer1_init();   
  }
  if(count==2)
  {
    Time_period=TCNT1*0.0000641026;
    TCNT1=0;
    count=1;
    Present_rpm=30/Time_period;

    Error = Required_rpm - Present_rpm; 
    H = Error * Dt;
    I_error = I_error + H;
    I = Error - Previous_error;
    D_error = I / Dt;
    P = P_gain * Error;
    I = I_gain * I_error;
    D = D_gain * D_error;
    Total_error = P + I + D;
    Previous_error = Error;
    Acc = Acc + Total_error;

    if(Acc<=107 && Acc>=20)
    {
      Final = Acc*2.38;
      if(Present_rpm == Required_rpm)
      {
        I_error=0;
      }
    }
    else if(Acc<30)
    {
      Final=70;
    }
    else if(Acc>107)
    {
      Final=255;
    }
//Serial.println(Present_rpm);
   }
}
