// 'roboface' example sketch for Adafruit I2C 8x8 LED backpacks:
//
//  www.adafruit.com/products/870   www.adafruit.com/products/1049
//  www.adafruit.com/products/871   www.adafruit.com/products/1050
//  www.adafruit.com/products/872   www.adafruit.com/products/1051
//  www.adafruit.com/products/959   www.adafruit.com/products/1052
//
// Requires Adafruit_LEDBackpack and Adafruit_GFX libraries.
// For a simpler introduction, see the 'matrix8x8' example.
//
// This sketch demonstrates a couple of useful techniques:
// 1) Addressing multiple matrices (using the 'A0' and 'A1' solder
//    pads on the back to select unique I2C addresses for each).
// 2) Displaying the same data on multiple matrices by sharing the
//    same I2C address.
//
// This example uses 5 matrices at 4 addresses (two share an address)
// to animate a face:
//
//     0     0
//
//      1 2 3
//
// The 'eyes' both display the same image (always looking the same
// direction -- can't go cross-eyed) and thus share the same address
// (0x70).  The three matrices forming the mouth have unique addresses
// (0x71, 0x72 and 0x73).
//
// The face animation as written is here semi-random; this neither
// generates nor responds to actual sound, it's simply a visual effect
// Consider this a stepping off point for your own project.  Maybe you
// could 'puppet' the face using joysticks, or synchronize the lips to
// audio from a Wave Shield (see wavface example).  Currently there are
// only six images for the mouth.  This is often sufficient for simple
// animation, as explained here:
// http://www.idleworm.com/how/anm/03t/talk1.shtml
//
// Adafruit invests time and resources providing this open source code,
// please support Adafruit and open-source hardware by purchasing
// products from Adafruit!
//
// Written by P. Burgess for Adafruit Industries.
// BSD license, all text above must be included in any redistribution.
//#include <Arduino.h>
//#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
//#include "Adafruit_GFX.h"

#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32.h>

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

// Left Motor
int dir1PinA = 2;
int dir2PinA = 3;
int speedPinA = 9;

// Right Motor
int dir1PinB = 4;
int dir2PinB = 5;
int speedPinB = 10;

ros::NodeHandle  nh;
float forwardMultiply = 1;
float backwardMultiply = 1;
float rotationMultiply = 1;

long duration = 0;
long timestamp = 0;
boolean isTimestampTaken = false;


void messageCb( const geometry_msgs::Twist& msg) {
  float leftSpeed;
  float rightSpeed;
  if( msg.linear.x  <=0.001 && msg.linear.x >= -0.001) {
    rightSpeed = MIN(msg.angular.z*255*rotationMultiply,255);
    leftSpeed = MIN(msg.angular.z * -255*rotationMultiply,255);
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

ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel_mux/input/teleop", messageCb );
ros::Subscriber<std_msgs::Float32> sub1("/set_forward_multiply", setForwardMul );
ros::Subscriber<std_msgs::Float32> sub2("/set_backward_multiply", setBackwardMul );
ros::Subscriber<std_msgs::Float32> sub3("/set_rotation_multiply", setRotationMul );



void setup() {
  
  // Seed random number generator from an unused analog input:
  randomSeed(analogRead(A0));

  // Initialize each matrix object:
  matrix.begin(matrixAddr);
  // If using 'small' (1.2") displays vs. 'mini' (0.8"), enable this:
  // matrix[i].setRotation(3);
  
  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(dir1PinA, OUTPUT);
  pinMode(dir2PinA, OUTPUT);
  pinMode(speedPinA, OUTPUT);
  pinMode(dir1PinB, OUTPUT);
  pinMode(dir2PinB, OUTPUT);
  pinMode(speedPinB, OUTPUT);

}

void setRightMotorSpeed(int speed)
{
  if (speed < 0) {
    digitalWrite(dir1PinA, HIGH);
    digitalWrite(dir2PinA, LOW);
    speed *= -1;
    speed = speed*backwardMultiply < -255 ? -255 : speed*backwardMultiply ;

  } 
  else {
    digitalWrite(dir1PinA, LOW);
    digitalWrite(dir2PinA, HIGH);
    speed = speed*forwardMultiply > 255 ? 255 : speed*backwardMultiply ;

  }
  
  analogWrite(speedPinA, speed);
}

void setLeftMotorSpeed(int speed)
{
  if (speed < 0) {
    digitalWrite(dir1PinB, HIGH);
    digitalWrite(dir2PinB, LOW);
    speed *= -1;
    speed = speed*backwardMultiply < -255 ? -255 : speed*backwardMultiply ;

  } 
  else {
    digitalWrite(dir1PinB, LOW);
    digitalWrite(dir2PinB, HIGH);
    speed = speed*forwardMultiply > 255 ? 255 : speed*backwardMultiply ;

  }
  analogWrite(speedPinB, speed);
}

void loop() {

  // this one doesn't have the button functionality, but the code should be easy to port. 
  //if(button is pressed) //you execute all the code below. from the spinOnce() to matrix.writeDisplay(); 
  //else{ // no display on the leds
    //turn the motors off
    //matrix.clear();
    //matrix.writeDisplay();
    //}
  nh.spinOnce();
  delay(1);

  if(!isTimestampTaken)
  {
    isTimestampTaken = true;
    timestamp = millis();  
  }
  duration = millis()-timestamp;

  if(duration > 20)
  {
    isTimestampTaken = false;
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



