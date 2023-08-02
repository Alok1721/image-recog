#include <PID_v1.h>

const int leftSensorPin = A0;   // Analog pin for left sensor
const int rightSensorPin = A1;  // Analog pin for right sensor
const int leftMotorPin = 9;     // Digital pin for left motor
const int rightMotorPin = 10;   // Digital pin for right motor

// Define PID gains
double KP = 5.0;  // Proportional gain
double KI = 0.1;  // Integral gain
double KD = 0.2;  // Derivative gain

// Define PID input, output, and setpoint variables
double leftSensorValue, rightSensorValue;
double input, output, setpoint;

// Define PID controller object
PID pid(&input, &output, &setpoint, KP, KI, KD, DIRECT);

void setup() {
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);

  // Initialize PID tuning parameters
  pid.SetSampleTime(50); // Time interval in milliseconds for PID computation
  pid.SetOutputLimits(-255, 255); // Limit the PID output to control motor speeds

  // Set the desired setpoint to the midpoint between the sensor values
  setpoint = (analogRead(leftSensorPin) + analogRead(rightSensorPin)) / 2.0;

  // Initialize the PID controller
  pid.SetMode(AUTOMATIC);
}

void loop() {
  // Read sensor values
  leftSensorValue = analogRead(leftSensorPin);
  rightSensorValue = analogRead(rightSensorPin);

  // Calculate the average sensor value as the input for PID control
  input = (leftSensorValue + rightSensorValue) / 2.0;

  // Calculate the error as the difference between input and setpoint
  double error = setpoint - input;

  // Compute the PID control output
  pid.Compute();

  // Calculate motor speeds based on PID output and set turning directions
  int leftSpeed = abs(output);
  int rightSpeed = abs(output);

  if (output > 0) {
    // Turn left
    digitalWrite(leftMotorPin, LOW);
    digitalWrite(rightMotorPin, HIGH);
    analogWrite(leftMotorPin, leftSpeed);
    analogWrite(rightMotorPin, rightSpeed);
  } else {
    // Turn right
    digitalWrite(leftMotorPin, HIGH);
    digitalWrite(rightMotorPin, LOW);
    analogWrite(leftMotorPin, leftSpeed);
    analogWrite(rightMotorPin, rightSpeed);
  }
}
