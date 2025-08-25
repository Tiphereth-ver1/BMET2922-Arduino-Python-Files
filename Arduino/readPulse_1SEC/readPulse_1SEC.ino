/*
** Scheduler provides teh framework to run tasks at regular times.
** Time is based on a delta from the previous micros() value. 
**
** Original Author:  Greg Watkins
** Date:    27 Aug 2021
** Updated by: Daniel Babekuhl
** Date:    14 Aug 2022
*/

#include "switch.h"

// pins for LED and switch
#define LED_PIN 32
#define SWITCH_PIN 35
#define SENSOR_PIN 25

// holds tick time counts
unsigned long lastTickTime;

void setup() {
  // initialize pin modes
  pinMode(LED_PIN, OUTPUT);
  pinMode(SWITCH_PIN, INPUT);
  
  // start the Serial interface (over USB)
  Serial.begin(115200);
  // a small delay to ensure that all messages are seen in the Serial Monitor.
  delay(1000);  
  Serial.println("\nSCHEDULER\n");

  lastTickTime = micros();
}



// Define switch data
// require 10 consecutive same-state readings before validating switch push
#define DEBOUNCE_CNT 10 
Switch switch1(1, DEBOUNCE_CNT);

// TICK/SCHEDULING DATA
// 200000 microseconds in 20 milliseconds
#define TICK_20MSEC 20000
 
// to count ticks to 1 sec
uint16_t tick1sec = 0;  
#define TICK_1SEC 50

// to count ticks to 10 sec
uint16_t tick10sec = 0; 
#define TICK_10SEC 500

// accumulate seconds for a time of day (ToD) clock
uint16_t secondsToD = 0;
uint16_t secondsCounter = 0;
uint16_t minutesCounter = 0;
uint16_t hoursCounter = 0;
bool latching_1 = false;
uint16_t sensor_reading;


void calculatetime() {
  hoursCounter = (secondsToD/3600)%24;
  minutesCounter = (secondsToD/60)%60;
  secondsCounter = secondsToD%60;
}

void loop() {
  
  if ((micros() - lastTickTime) > TICK_20MSEC) {
    // save current time immediately. This preserves timing accuracy indpendent
    // of the execution time of the code below. This is moe accurate than using the 
    // delay() function.
    lastTickTime = micros();  
    //*********************** 20 msec tasks *********************
    
    // can update/check status in one statement
    // if (switch1.update(digitalRead(SWITCH_PIN))) {
    //   Serial.printf("Switch %x ->%x\n", switch1.id(), switch1.state());
    // }


    //>>>>> Insert code here so that each switch operates as a push on/push off switch rather than momentary contact
    // what is happening on this line?
    if (switch1.update(digitalRead(SWITCH_PIN))) //check if the switch is being an
    {
    // Serial.printf("New switch state: ->%x\n", switch1.state());
    if (switch1.state())//only run the next line if the switch is toggled to true state (will not do anything if the switch is toggled off)
    {
    latching_1 = !latching_1; //changes switch boolean
    Serial.printf("Latching signal state -> %x\n", latching_1);
    }
    }
}
    
    //************************************************************



    //*********************** 1 sec tasks *********************
    if (++tick1sec >= TICK_1SEC) {
      // execute 1 second tasks
      // Serial.printf("\nTICK1: %.3f microsec\n", micros()*1.);
      tick1sec = 0;

      secondsToD++;  // update time of day

    sensor_reading = analogRead(SENSOR_PIN);
    Serial.printf("%d\n", sensor_reading);
    //************************************************************
    }


    //*********************** 10 sec tasks *********************
    if (++tick10sec >= TICK_10SEC) {
      Serial.printf("\nTICK10: %.3f sec\n", millis()/1000.);
      calculatetime();
      Serial.printf("Time elapsed - %02d:%02d:%02d \n", hoursCounter, minutesCounter, secondsCounter);
      
      tick10sec = 0;
    }
    //************************************************************

  } // 20 msec tick
