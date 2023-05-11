#include <Servo.h>
Servo myServo;

int potentPin = A2;
int potent = 0;
int degree = 0;

int enableAPin = 6;
int in1Pin = 7;
int in2Pin = 8;
int in3Pin = 9;
int in4Pin = 10;
int enableBPin = 5;

void setup()
{
  Serial.begin(9600);
  myServo.attach(13);  // attaches the servo on pin 9 to the servo object
  pinMode(potentPin, INPUT);
  pinMode(enableAPin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(enableBPin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);
  //The problem with TT gear motors is that, at very low pwm value it does not even rotate.
  //If we increase the PWM value then it rotates faster and our robot is not controlled in that speed and goes out of line.
  //For that we need to increase the frequency of analogWrite.
  //Below line is important to change the frequency of PWM signal on pin D5 and D6
  //Because of this, motor runs in controlled manner (lower speed) at high PWM value.
  //This sets frequecny as 7812.5 hz.
  TCCR0B = TCCR0B & B11111000 | B00000010 ;
}

void loop()
{
  int motorPWMSpeed = 0;
  int joystickValue = analogRead(A0);   //Joystick gives values ranging from 0 to 1023. So we will consider center value as 512 and lets keep some deadband at center.
  int joystickValue2 = analogRead(A1);
  potent = analogRead(potentPin);
  degree = round(potent / 11.4); //control the angle between 0 to 90 degrees
  myServo.write(degree);
  delay(15);
  Serial.println(degree);

  if (joystickValue >= 530)           //This will move motor in forward direction  
  {
    motorPWMSpeed = map(joystickValue, 530, 1023, 0, 255);
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);    
    analogWrite(enableAPin, motorPWMSpeed);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);    
    analogWrite(enableBPin, motorPWMSpeed);
  }
  else if (joystickValue <= 490)      //This will move motor in reverse direction    
  {
    motorPWMSpeed = map(joystickValue, 490, 0, 0, 255);
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);    
    analogWrite(enableAPin, motorPWMSpeed);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, HIGH);    
    analogWrite(enableBPin, motorPWMSpeed);
  }  

  else if (joystickValue2 >= 530)           //This will move motor in forward direction  
  {
    motorPWMSpeed = map(joystickValue2, 530, 1023, 0, 255);
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);    
    analogWrite(enableAPin, motorPWMSpeed);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);    
    analogWrite(enableBPin, motorPWMSpeed);
  }
  else if (joystickValue2 <= 490)      //This will move motor in reverse direction    
  {
    motorPWMSpeed = map(joystickValue2, 490, 0, 0, 255);
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);    
    analogWrite(enableAPin, motorPWMSpeed);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, HIGH);    
    analogWrite(enableBPin, motorPWMSpeed);
  }  
  else                                //Stop the motor
  {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, LOW);     
  }
}
