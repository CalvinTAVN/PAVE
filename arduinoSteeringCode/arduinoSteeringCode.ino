 	// LINEAR ACTUATOR PINS (lin actuator 1)
// RPWM on motor controler, extends pin when high
const int LaExtendPin1 = 11;  //if this pin's value is between 0 and 255, it extends (retract is zero)
// LPWM on motor controler, retracts pin when high
const int LaRetractPin1 = 10;  //if this pin's value is between 0 and 255, it retracts (extend is zero)
// Analog position pin on linear actuator
const int LaPositionPin1 = A2;  //this pin outputs the analog position of the linear actuator
// linear actuator one is true
const bool La1 = true;




// LINEAR ACTUATOR PIN (lin actuator 2)
// RPWM on motor controler, extends pin when high
const int LaExtendPin2 = 6;
// LPWM on motor controler, retracts pin when high
const int LaRetractPin2 = 5;
// Analog position pin on linear actuator
const int LaPositionPin2 = A3;
// linear actuator two is false
const bool La2 = false;




// CONSTANT VALUES
// All positions are mapped with this as the min value
const int MAP_MIN_VALUE = 0;
// All positions are mapped with this as the max value
const int MAP_MAX_VALUE_1 = 80;
const int MAP_MAX_VALUE_2 = 80;
// Position of actuators when boat is going straight
const int CENTER_VALUE = 17; //(CENTER_VALUE SHOULD BE 17/80 OF MAP_MAX_VALUE)








// definees forward actuation as true
const bool FORWARD = true;
// defines backward actuation as false
const bool BACKWARD = false;
// analog linear actuator value (when it's fully retracted)
const int ACTUATOR_ANALOG_MINVALUE = 73;
// analog linear actuator value (when it's fully extended)
const int ACTUATOR_ANALOG_MAXVALUE = 709;




// CHANGING VALUES
// acuator 1 position according to analog in
int actuator_Analog_Position_1;
// mapped actuator 1 position
int actuator_Mapped_Position_1;
// acuator 2 position according to analog in
int actuator_Analog_Position_2;
// mapped actuator 2 position
int actuator_Mapped_Position_2;




/***
--- variables for control ---
***/
// This variable will increase or decrease depending on the rotation of encoder
volatile signed int unmapped_Wanted_Position = 0;
// mapped wanted positions for each actuators
volatile int mapped_Wanted_Position_1 = CENTER_VALUE;
volatile int mapped_Wanted_Position_2 = CENTER_VALUE;


// COMMENTS
int distance_to_Wanted_Position_1;
int distance_to_Wanted_Position_2;




// preliminary setup
void setup() {
 Serial.begin(9600);
 Serial.setTimeout(10);


 //linear actuator pinout
 //configures the extend and retract pin as outputs
 pinMode(LaExtendPin1, OUTPUT);
 pinMode(LaRetractPin1, OUTPUT);
 pinMode(LaExtendPin2, OUTPUT);
 pinMode(LaRetractPin2, OUTPUT);




 // turns off all linear actuators
 analogWrite(LaExtendPin1, 0);
 analogWrite(LaRetractPin1, 0);
 analogWrite(LaExtendPin2, 0);
 analogWrite(LaRetractPin2, 0);
 mapped_Wanted_Position_1 = CENTER_VALUE;
 mapped_Wanted_Position_2 = CENTER_VALUE;


}




//given an actuator, direction and speed, start actuating arm.
void actuate(bool whichActuator, bool direc, int speed) {
 if (whichActuator) {
   //direc == true == forward, direc == false == backward
   if (direc) {  //if the direction is forward, set the extend to a given speed
     analogWrite(LaExtendPin1, speed);
     analogWrite(LaRetractPin1, 0);
   } else {  //if the direction is backward, set the retract pin to that given speed
     analogWrite(LaRetractPin1, speed);
     analogWrite(LaExtendPin1, 0);
   }
 } else {
   if (direc) {  //if the direction is forward, set the extend to a given speed
     analogWrite(LaRetractPin2, speed);
     analogWrite(LaExtendPin2, 0);
   } else {  //if the direction is backward, set the retract pin to that given speed
     analogWrite(LaExtendPin2, speed);
     analogWrite(LaRetractPin2, 0);
   }
 }
}








void loop() {
 //this is the position that is read from the linear actuator
 actuator_Analog_Position_1 = analogRead(LaPositionPin1);
 //this is the position that is read from the linear actuator
 actuator_Analog_Position_2 = analogRead(LaPositionPin2);
 //remaps the actual location (272->1000 to 0 50)
 //maps the location of the actuator to a value of 0 to 50
 actuator_Mapped_Position_1 = map(actuator_Analog_Position_1, ACTUATOR_ANALOG_MINVALUE,
                                  ACTUATOR_ANALOG_MAXVALUE, MAP_MIN_VALUE, MAP_MAX_VALUE_1);
 //maps the location of the actuator to a value of 0 to 50
 actuator_Mapped_Position_2 = map(actuator_Analog_Position_2, ACTUATOR_ANALOG_MINVALUE,
                                  ACTUATOR_ANALOG_MAXVALUE, MAP_MIN_VALUE, MAP_MAX_VALUE_2);


 if (Serial.available() > 0) {
   unmapped_Wanted_Position = Serial.parseInt(SKIP_ALL);
   //unmapped_Wanted_Position = 500;


 }

 // position = wantedPosition - centerValue
 // position = wantedPosition - centerValue
mapped_Wanted_Position_1 = min(map(unmapped_Wanted_Position, 0, 1000, MAP_MIN_VALUE, 2*CENTER_VALUE), 75);                    //dominant, so add position
mapped_Wanted_Position_2 = min(2*CENTER_VALUE - map(unmapped_Wanted_Position, 0, 1000, MAP_MIN_VALUE, 2*CENTER_VALUE), 2*CENTER_VALUE);  //recessive, so subtract position


 //wanted position is the target
 distance_to_Wanted_Position_1 = mapped_Wanted_Position_1 - actuator_Mapped_Position_1;
 distance_to_Wanted_Position_2 = (mapped_Wanted_Position_2 - actuator_Mapped_Position_2);






 //Serial.println("   actuator_Analog_Position_1: " + String(actuator_Analog_Position_1) + "  actuator_Mapped_Position_1: " + String(actuator_Mapped_Position_1) + "  unmapped_Wanted_Position: " + String(unmapped_Wanted_Position) + "  wantedPosition_1: " + String(mapped_Wanted_Position_1) + "   distance_to_Wanted_Position_1: " + String(distance_to_Wanted_Position_1));
 //Serial.println("   actuator_Analog_Position_2: " + String(actuator_Analog_Position_2) + "  actuator_Mapped_Position_2: " + String(actuator_Mapped_Position_2) + "  unmapped_Wanted_Position: " + String(unmapped_Wanted_Position) + "  wantedPosition_2: " + String(mapped_Wanted_Position_2) + "   distance_to_Wanted_Position_2: " + String(distance_to_Wanted_Position_2));






//proportional
if (distance_to_Wanted_Position_1 == 0) {
  actuate(La1, FORWARD, 0);
} else if (distance_to_Wanted_Position_1 > MAP_MAX_VALUE_1 / 15) {  //if the mapped actuator location isn't
  actuate(La1, FORWARD, 255);                                      //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_1 < -1 * (MAP_MAX_VALUE_1 / 15)) {
  actuate(La1, BACKWARD, 255);  //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_1 > 0) {
  actuate(La1, FORWARD, 255 / 4);  //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_1 < 0) {
  actuate(La1, BACKWARD, 255 / 4);  //actauates at full velocity (bang)
}




if (distance_to_Wanted_Position_2 == 0) {
  actuate(La2, BACKWARD, 0);
} else if (distance_to_Wanted_Position_2 > MAP_MAX_VALUE_2 / 15) {  //if the mapped actuator location isn't
  actuate(La2, BACKWARD, 255);                                      //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_2 < -1 * (MAP_MAX_VALUE_2 / 15)) {
  actuate(La2, FORWARD, 255);  //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_2 > 0) {
  actuate(La2, BACKWARD, 255 / 4);  //actuates at full velocity (bang)
} else if (distance_to_Wanted_Position_2 < 0) {
  actuate(La2, FORWARD, 255 / 4);  //actuates at full velocity (bang)
}
}

