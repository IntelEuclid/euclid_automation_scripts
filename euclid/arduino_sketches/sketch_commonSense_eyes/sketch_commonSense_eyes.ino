#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32.h>
//#include <SoftwareSerial.h>

//#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

#define MIN(x,y) ((x) < (y) ? (x) : (y))
#define MAX(x,y) ((x) > (y) ?( x) : (y))


// Because the two eye matrices share the same address, only one
// matrix object is needed for the displays:

Adafruit_8x8matrix matrix = Adafruit_8x8matrix();

static const uint8_t matrixAddr =  0x70;

static const uint8_t PROGMEM // Bitmaps are stored in program memory
  blinkImg[][8] = {    // Eye animation frames
  { B00000000,         // Fully open eye
    B00111100,
    B01111110,
    B01111110,
    B01111110,
    B01111110,
    B00111100,
    B00000000 },
  { B00000000,
    B00000000,
    B01111110,
    B01111110,
    B01111110,
    B01111110,
    B00111100,
    B00000000 },
  { B00000000,
    B00000000,
    B00111100,
    B01111110,
    B01111110,
    B01111110,
    B00111100,
    B00000000 },
  { B00000000,
    B00000000,
    B00000000,
    B00111100,
    B01111110,
    B01111110,
    B00011000,
    B00000000 },
  { B00000000,         // Fully closed eye
    B00000000,
    B00000000,
    B00000000,
    B01000010,
    B00111100,
    B00000000,
    B00000000 } };
    
uint8_t
  blinkIndex[] = { 1, 2, 3, 4, 3, 2, 1 }, // Blink bitmap sequence
  blinkCountdown = 100, // Countdown to next blink (in frames)
  gazeCountdown  =  75, // Countdown to next eye movement
  gazeFrames     =  50; // Duration of eye movement (smaller = faster)
int8_t
  eyeX = 3, eyeY = 3,   // Current eye position
  newX = 3, newY = 3,   // Next eye position
  dX   = 0, dY   = 0;   // Distance from prior to new position

//#define BLUETOOTH_SPEED 9600
//
//// Swap RX/TX connections on bluetooth chip
////   Pin 12 --> Bluetooth TX
////   Pin 13 --> Bluetooth RX
//SoftwareSerial mySerial(12, 13); // RX, TX

long eyeFramerateDuration = 0;
long eyeFramerateTimestamp = 0;
boolean isEyeFramerateTimestampTaken = false;

// Left Motor
int dir1PinA = 2;
int dir2PinA = 3;
int speedPinA = 9;

// Right Motor
int dir1PinB = 4;
int dir2PinB = 5;
int speedPinB = 10;

//BTN
int btn_Pin = 8;

ros::NodeHandle  nh;
float forwardMultiply = 1;
float backwardMultiply = 1;
float rotationMultiply = 1;

float leftGain = 1;
float rightGain = 1;

void messageCb( const geometry_msgs::Twist& msg) {
  float leftSpeed;
  float rightSpeed;
  if ( msg.linear.x  <= 0.001 && msg.linear.x >= -0.001) {
    rightSpeed = MIN(msg.angular.z * 255 * rotationMultiply, 255);
    leftSpeed = MIN(msg.angular.z * -255 * rotationMultiply, 255);
  }
  else {
    rightSpeed = MIN(MAX(-255, msg.linear.x * 255.0 + msg.angular.z * 60.0), 255);
    leftSpeed = MIN(MAX(-255, msg.linear.x * 255.0 - msg.angular.z * 60.0), 255);
  }
  setLeftMotorSpeed(leftSpeed);
  setRightMotorSpeed(rightSpeed);
}

void setForwardMul( const std_msgs::Float32& msg) {
  forwardMultiply = msg.data;
}

void setBackwardMul( const std_msgs::Float32& msg) {
  backwardMultiply = msg.data;
}

void setRotationMul( const std_msgs::Float32& msg) {
  rotationMultiply = msg.data;
}

void setRightGain( const std_msgs::Float32& msg) {
  rightGain = msg.data;
}
void setLeftGain( const std_msgs::Float32& msg) {
  leftGain = msg.data;
}


ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel_mux/input/teleop", messageCb );
ros::Subscriber<std_msgs::Float32> sub1("/set_forward_multiply", setForwardMul );
ros::Subscriber<std_msgs::Float32> sub2("/set_backward_multiply", setBackwardMul );
ros::Subscriber<std_msgs::Float32> sub3("/set_rotation_multiply", setRotationMul );

ros::Subscriber<std_msgs::Float32> sub4("/set_right_gain", setRightGain );
ros::Subscriber<std_msgs::Float32> sub5("/set_left_gain", setLeftGain );


void setup() {

  // Seed random number generator from an unused analog input:
  randomSeed(analogRead(A0));

  // Initialize each matrix object:
  matrix.begin(matrixAddr);
  //--- Init BT
  //  mySerial.begin(BLUETOOTH_SPEED);
  delay(1000);

  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  nh.subscribe(sub4);
  nh.subscribe(sub5);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(dir1PinA, OUTPUT);
  pinMode(dir2PinA, OUTPUT);
  pinMode(speedPinA, OUTPUT);
  pinMode(dir1PinB, OUTPUT);
  pinMode(dir2PinB, OUTPUT);
  pinMode(speedPinB, OUTPUT);

  //Btn
  pinMode(btn_Pin, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  

}

void setRightMotorSpeed(int speed)
{
  speed = speed * rightGain;
  if (speed < 0) {
    digitalWrite(dir1PinA, HIGH);
    digitalWrite(dir2PinA, LOW);
    speed *= -1;
    speed = speed * backwardMultiply < -255 ? -255 : speed * backwardMultiply ;

  }
  else {
    digitalWrite(dir1PinA, LOW);
    digitalWrite(dir2PinA, HIGH);
    speed = speed * forwardMultiply > 255 ? 255 : speed * forwardMultiply ;

  }

  analogWrite(speedPinA, speed);
}

void setLeftMotorSpeed(int speed)
{

  speed = speed * leftGain;
  if (speed < 0) {
    digitalWrite(dir1PinB, HIGH);
    digitalWrite(dir2PinB, LOW);
    speed *= -1;
    speed = speed * backwardMultiply < -255 ? -255 : speed * backwardMultiply ;

  }
  else {
    digitalWrite(dir1PinB, LOW);
    digitalWrite(dir2PinB, HIGH);
    speed = speed * forwardMultiply > 255 ? 255 : speed * forwardMultiply ;

  }
  analogWrite(speedPinB, speed);
}

void loop() {

  int csAttached = digitalRead(btn_Pin);

  if (csAttached == LOW) {
    digitalWrite(13, HIGH);
    nh.spinOnce();
    delay(1);
    //******************
  //delay(20); // ~50 FPS   // haven't tested if the delay will cause problems, but could be replaced with ros.sleep().
  if(!isEyeFramerateTimestampTaken)
  {
    isEyeFramerateTimestampTaken = true;
    eyeFramerateTimestamp = millis();
  }
  eyeFramerateDuration = millis()- eyeFramerateTimestamp;
  
  if(eyeFramerateDuration > 19) //20 millisecond delay for eye framerate
  {
    isEyeFramerateTimestampTaken = false;
    
        // Draw eyeball in current state of blinkyness (no pupil).  Note that
  // only one eye needs to be drawn.  Because the two eye matrices share
  // the same address, the same data will be received by both.
  matrix.clear();
  // When counting down to the next blink, show the eye in the fully-
  // open state.  On the last few counts (during the blink), look up
  // the corresponding bitmap index.
  matrix.drawBitmap(0, 0,
    blinkImg[
      (blinkCountdown < sizeof(blinkIndex)) ? // Currently blinking?
      blinkIndex[blinkCountdown] :            // Yes, look up bitmap #
      0                                       // No, show bitmap 0
    ], 8, 8, LED_ON);
  // Decrement blink counter.  At end, set random time for next blink.
  if(--blinkCountdown == 0) blinkCountdown = random(5, 180);

  // Add a pupil (2x2 black square) atop the blinky eyeball bitmap.
  // Periodically, the pupil moves to a new position...
  if(--gazeCountdown <= gazeFrames) {
    // Eyes are in motion - draw pupil at interim position
    matrix.fillRect(
      newX - (dX * gazeCountdown / gazeFrames),
      newY - (dY * gazeCountdown / gazeFrames),
      2, 2, LED_OFF);
    if(gazeCountdown == 0) {    // Last frame?
      eyeX = newX; eyeY = newY; // Yes.  What's new is old, then...
      do { // Pick random positions until one is within the eye circle
        newX = random(7); newY = random(7);
        dX   = newX - 3;  dY   = newY - 3;
      } while((dX * dX + dY * dY) >= 10);      // Thank you Pythagoras
      dX            = newX - eyeX;             // Horizontal distance to move
      dY            = newY - eyeY;             // Vertical distance to move
      gazeFrames    = random(3, 15);           // Duration of eye movement
      gazeCountdown = random(gazeFrames, 120); // Count to end of next movement
    }
  } else {
    // Not in motion yet -- draw pupil at current static position
    matrix.fillRect(eyeX, eyeY, 2, 2, LED_OFF);
  }


  // Refresh the matrices 
  matrix.writeDisplay();
  } 
  }
  else {
    digitalWrite(13, LOW);

    analogWrite(speedPinB, 0);
    analogWrite(speedPinA, 0);
    
        // Draw eyeball in current state of blinkyness (no pupil).  Note that
  // only one eye needs to be drawn.  Because the two eye matrices share
  // the same address, the same data will be received by both.
  matrix.clear();

  // Refresh the matrices 
  matrix.writeDisplay();
  
  }
}

