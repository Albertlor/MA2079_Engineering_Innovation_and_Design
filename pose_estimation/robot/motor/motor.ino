#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 100;    // variable to store the servo position

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

long duration1; // variable for the duration of sound wave travel
int distance1; // variable for the distance measurement
int count_stop = 0;

char recvChar;                                        //variable to store character received
SoftwareSerial blueToothSerial(RxD,TxD);              //bluetooth device acts as a serial communication device
                                                      //receive and transmit with respect to the Arduino board

//TT motors
int enA = 6;  //Right Wheel Speed
int in1 = 7;  //Right Wheel Direction
int in2 = 8;  //Right Wheel Direction

int enB = 5;  //Left Wheel Speed
int in3 = 9;  //Left Wheel Direction
int in4 = 10; //Left Wheel Direction

int motor_speedA = 185;  //optimal speed = 176 and for turning 174*0.942
int motor_speedB = 135;
char stall = ' ';
int count = 0;
int temp = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  myservo.attach(13);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT

  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin1, INPUT); // Sets the echoPin as an INPUT
  
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");
  Serial.println("Ultrasonic Sensor HC-SR04 Test1"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");

  pinMode(RxD, INPUT);                              //set mode of receive pin (from bluetooth)
  pinMode(TxD, OUTPUT);                             //set mode of transmit pin (to bluetooth)
  blueToothSerial.begin(9600);                      //start the bluetooth serial "port"

  //The problem with TT gear motors is that, at very low pwm value it does not even rotate.
  //If we increase the PWM value then it rotates faster and our robot is not controlled in that speed and goes out of line.
  //For that we need to increase the frequency of analogWrite.
  //Below line is important to change the frequency of PWM signal on pin D5 and D6
  //Because of this, motor runs in controlled manner (lower speed) at high PWM value.
  //This sets frequecny as 7812.5 hz.
  TCCR0B = TCCR0B & B11111000 | B00000010 ;
  
  //TT motor
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  //IR sensor
  pinMode(left, INPUT);
  pinMode(right, INPUT);
}

void loop() {
  digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    analogWrite (enA, motor_speedA);
    analogWrite (enB, motor_speedA);
}
