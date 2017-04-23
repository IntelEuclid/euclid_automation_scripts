
int pinI1 = 2; //define IN1
int pinI2 = 3; //define IN2
int leftSpeed = 9; //define EA(PWM)

int pinI3 = 4; //define IN3
int pinI4 = 5; //define IN4
int rightSpeed = 10; //define EB(PWM)


void setup() {  // Setup runs once per reset
  // initialize serial communication @ 9600 baud:
  Serial.begin(9600);

  pinMode(pinI1, OUTPUT);
  pinMode(pinI2, OUTPUT);
  pinMode(leftSpeed, OUTPUT);

  pinMode(pinI3, OUTPUT);
  pinMode(pinI4, OUTPUT);
  pinMode(rightSpeed, OUTPUT);
}

void leftMotorForward(int speed)
{
 
  digitalWrite(pinI1, LOW);
  digitalWrite(pinI2, HIGH);
   analogWrite(leftSpeed, speed);
  Serial.println("leftMotor FW");
}

void leftMotorBackward(int speed)
{
  digitalWrite(pinI1, HIGH);
  digitalWrite(pinI2, LOW);
  analogWrite(leftSpeed, speed);

  Serial.println("leftMotor REV");
}

void rightMotorForward(int speed)
{
 
  digitalWrite(pinI3, LOW);
  digitalWrite(pinI4, HIGH);
   analogWrite(rightSpeed, speed);
  Serial.println("rightMotor FW");
}

void rightMotorBackward(int speed)
{
  analogWrite(rightSpeed, speed);
  digitalWrite(pinI3, HIGH);
  digitalWrite(pinI4, LOW);
  Serial.println("rightMotor 2 REV");
}

void leftMotorStop()
{
  analogWrite(leftSpeed, 0);
  digitalWrite(pinI1, HIGH);
  digitalWrite(pinI2, HIGH);
  Serial.println("leftMotor Stop");
}

void rightMotorStop()
{
  analogWrite(rightSpeed, 0);
  digitalWrite(pinI4, HIGH);
  digitalWrite(pinI3, HIGH);
  Serial.println("rightMotor Stop");
}


void stop()
{
  leftMotorStop();
  rightMotorStop();
}

void loop() {

  //stop();
  //delay(1000);
  rightMotorForward(100);
  
  delay(2000);
  //stop();
  rightMotorBackward(100);
  delay(2000);
  rightMotorStop();
  leftMotorForward(100);
  delay(2000);
  leftMotorBackward(100);
  delay(2000);
  leftMotorStop();
  
}
