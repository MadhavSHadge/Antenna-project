#include <Arduino.h>

const int enablePin = 9;  // PWM pin for motor speed control
const int int1Pin = 8;    // Motor driver input 1
const int int2Pin = 7;    // Motor driver input 2

int speed = 0;  // Global variable to hold speed

int encoderPin1 = 2;
int encoderPin2 = 3;

volatile int lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;

int pulses = 0;
int initialPulse = 0;           //to test


void setup() {
  Serial.begin(9600);
  pinMode(enablePin, OUTPUT);
  pinMode(int1Pin, OUTPUT);
  pinMode(int2Pin, OUTPUT);

  pinMode(encoderPin1, INPUT); 
  pinMode(encoderPin2, INPUT);

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);
}


void loop() {

  if (Serial.available() > 0) {  // Check if data is available to read
    pulses = Serial.parseInt();  // Read the incoming data as integer
    Serial.print("Received pulses:");
    Serial.println(pulses);
    
    // Wait for the next input
    while (Serial.available() == 0) {}
    
    speed = Serial.parseInt();  // Read the incoming data as integer
    Serial.print("Received speed:");
    Serial.println(speed);
  }

{
  Serial.println(encoderValue);
  delay(1000); //just here to slow down the output, and show it will work  even during a delay
}
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read command from Serial
    switch (command) {
      case 'F':  // Forward
        forward(speed,pulses);  // Call forward function with current 'speed'
         Serial.println("Forward direction");
        break;
      case 'B':  // Backward
        backward(speed, pulses);  // Call backward function with current 'speed'
        Serial.println("Backward direction");
        break;
      case 'S':  // Stop
        stopMotor();
        Serial.println("Stop motor");
        break;
      case 'D':
        directionCheck(encoderValue);
        break;
    }
  }
}

void updateEncoder(){
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --;

  lastEncoded = encoded; //store this value for next time
}


void forward(int speed, int pulses) {                   //testing function
 while (encoderValue<=pulses){
  analogWrite(enablePin, speed);  // Set motor speed
  digitalWrite(int1Pin, HIGH);    // Set direction
  digitalWrite(int2Pin, LOW);
  Serial.println("Funtion call of forward direction");
   encoderValue++;
 }
 stopMotor();
}

void backward(int speed, int pulses) { 
 while (encoderValue<=pulses){
  analogWrite(enablePin, speed);  // Set motor speed
  digitalWrite(int1Pin, LOW);     // Set direction
  digitalWrite(int2Pin, HIGH);
  Serial.println("Funtion call of backward direction");
  encoderValue++;
 }
 stopMotor();
}

// Function to stop the motor
void stopMotor() {
  digitalWrite(int1Pin, LOW);
  digitalWrite(int2Pin, LOW);
  Serial.println("Funtion call of Stop motor");
}


void directionCheck(int encoderValue) {
  static int previousEncoderValue = 0;
  
  if (encoderValue > previousEncoderValue) {
    Serial.println("Clockwise Direction");
  } else if (encoderValue < previousEncoderValue) {
    Serial.println("Anti-Clockwise Direction");
  } else {
    Serial.println("No Change in Direction");
  }
  previousEncoderValue = encoderValue;
}
