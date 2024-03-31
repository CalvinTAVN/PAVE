
//all pinout for linear actuator
const int rc_pin = 7;
const int Extend_pin = 6;
const int Retract_pin = 5;
const int Position_pin = A1;
int RC_duration;
int RC_location;
int actual_location;
int deadband = 10;



// constant values
const int actual_minValue = 73;
const int actual_maxValue = 709;
const int RC_minValue = 0;
const int RC_maxValue = 50;
volatile int wanted_Position = 0;
const bool forward = true;
const bool backward = false;

//variables for rotary encoder
volatile signed int temp = 0; //This variable will increase or decrease depending on the rotation of encoder
volatile signed int counter = 0;
const int rotary_encoder_pin_1 = 2;
const int rotary_encoder_pin_2 = 3;   




void setup() {
Serial.begin(9600);

  //linear actuator pinout
  pinMode (rc_pin, INPUT);
  pinMode (Extend_pin, OUTPUT) ;
  pinMode (Retract_pin, OUTPUT);
  digitalWrite (Extend_pin, LOW) ;
  digitalWrite (Retract_pin, LOW) ;
  Serial.println("actual_location");
  pinMode (Position_pin, INPUT_PULLUP);
  


  //rotary encoder pinout
  pinMode(rotary_encoder_pin_1, INPUT_PULLUP); // internal pullup input pin 2
  pinMode(rotary_encoder_pin_2, INPUT_PULLUP); // internalเป็น pullup input pin 3 
  //A rising pulse from encodenren activated ai0(). AttachInterrupt 0 is DigitalPin nr 2 on moust Arduino.
  attachInterrupt(0, ai0, RISING);
  //B rising pulse from encodenren activated ai1(). AttachInterrupt 1 is DigitalPin nr 3 on moust Arduino.
  attachInterrupt(1, ai1, RISING);  
   


}

void ai0() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if(digitalRead(3)==LOW) {
  counter++;
  }else{
  counter--;
  }
  }
   
  void ai1() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if(digitalRead(2)==LOW) {
  counter--;
  }else{
  counter++;
  }
  }




//given a direction and speed, start actuating arm.
void actuate(bool direc, int speed) {
 //true == forward, false == backward
 if (direc) {
   analogWrite(Extend_pin, speed);
   analogWrite(Retract_pin, 0); 
 }
 else {
   analogWrite(Retract_pin, speed);
   analogWrite(Extend_pin, 0); 
 } 
}










void loop() {
 actual_location = analogRead(Position_pin);
 if( counter != temp ) {
  Serial.println (counter);
  temp = counter;
 }
 //remaps the actual location (272->1000 to 0 1000)
 RC_location = map (actual_location, actual_minValue, actual_maxValue, RC_minValue, RC_maxValue);


  Serial.println("RC_Location: " + String(RC_location) + "   Actual_Location: "+ String(actual_location) + "   counter: " + String(temp) + "  wantedPosition: " + String(wanted_Position));
  //Serial.println(digitalRead(Position_pin));



// if (Serial.available())
   //{
     // switch (Serial.read())
     // {
     //   case 'w':
     //     Serial.println("fullyForward");
     //     wanted_Position = 100;
     //     break;
     
     //   case 's':
     //     Serial.println("fullyBackwards");
     //     wanted_Position = 50;
     //     break;




     //   case 'd':
     //     Serial.println("middle");
     //     wanted_Position = 0;
     //     break;
   //   }


   wanted_Position = map((temp), -200, 200, RC_minValue, RC_maxValue);
   if (wanted_Position > RC_location) {
     actuate(forward, 255);
   }
   else if (wanted_Position < RC_location) {
     actuate(backward, 255);
   }
   else {
     actuate(forward, 0);
   }
 
 }





