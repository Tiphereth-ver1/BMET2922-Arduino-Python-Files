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
#define LED_PIN 25
#define LED_2 32
#define SWITCH_PIN 33
#define SENSOR_PIN 27

// holds tick time counts
unsigned long lastTickTime;
unsigned long previous;

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
uint16_t pulse_reading;
bool threshold = true;
bool state = true;

// ----- Adaptive-threshold HR detection -----
const uint16_t WINDOW_SAMPLES = 120;          // Number of samples per window (~2.4s at 20ms tick)
const uint16_t CONTACT_MIN_P2P = 180;         // Minimum peak-to-peak amplitude to consider valid contact
const uint16_t CONTACT_MIN_DC = 900;          // Minimum average DC level (filter out floating noise)
const uint16_t CONTACT_MAX_DC = 3300;         // Maximum average DC level (filter out saturation)
const unsigned long MIN_BEAT_INTERVAL = 320;  // Minimum beat-to-beat interval (ms) ~187 bpm
const unsigned long MAX_BEAT_INTERVAL = 1800; // Maximum beat-to-beat interval (ms) ~33 bpm
const uint8_t THRESH_FRACTION_PCT = 60;       // Threshold position between min and max (percentage)
const uint8_t HYSTERESIS_PCT = 10;            // Hysteresis width as percentage of amplitude
const unsigned long BPM_TIMEOUT_MS = 2500;    // Timeout (ms) to reset BPM to 0 if no beat detected
const uint8_t CONSIST_PEAKS = 3;              // Require N consistent beats before updating BPM

uint16_t rawMin = 4095, rawMax = 0;
uint16_t amplitude = 0;
uint16_t thresholdHigh = 0, thresholdLow = 0;
uint16_t windowCount = 0;

bool contact = false;
bool above = false;                 // State flag for hysteresis edge detection
unsigned long lastBeatMs = 0;
uint16_t bpm = 0;

// Store last intervals for consistency check
unsigned long lastIntervals[CONSIST_PEAKS] = {0};
uint8_t ivIdx = 0, ivCount = 0;


void calculatetime() {
  hoursCounter = (secondsToD/3600)%24;
  minutesCounter = (secondsToD/60)%60;
  secondsCounter = secondsToD%60;
}

bool pulseChange() {
      if (pulse_reading >2100) {
        digitalWrite(LED_PIN, HIGH);
        return true;
      }
      else {
        digitalWrite(LED_PIN, LOW);
        return false;
      }

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
    pulse_reading = analogRead(SENSOR_PIN);

    // Update running min/max values
    if (pulse_reading < rawMin) rawMin = pulse_reading;
    if (pulse_reading > rawMax) rawMax = pulse_reading;
    windowCount++;

    // Every window (~2.4 s), update contact state and thresholds
    if (windowCount >= WINDOW_SAMPLES) {
      amplitude = (rawMax > rawMin) ? (rawMax - rawMin) : 0;
      uint16_t dc = (rawMax + rawMin) / 2;

      // Check for valid finger contact
      contact = (amplitude >= CONTACT_MIN_P2P) &&
                (dc >= CONTACT_MIN_DC) &&
                (dc <= CONTACT_MAX_DC);

      if (contact) {
        uint16_t base = rawMin + (uint32_t)amplitude * THRESH_FRACTION_PCT / 100;
        uint16_t hyst = (uint32_t)amplitude * HYSTERESIS_PCT / 100;
        thresholdHigh = base;
        thresholdLow  = (base > hyst) ? (base - hyst) : base / 2;
      } else {
        bpm = 0;
        above = false;
      }

      // Reset window statistics
      rawMin = 4095; rawMax = 0; windowCount = 0;
    }

    // Hysteresis edge detection (only active with contact)
    if (contact) {
      bool nowAbove = above ? (pulse_reading > thresholdLow)
                            : (pulse_reading > thresholdHigh);

      // Rising edge = heartbeat
      if (nowAbove && !above) {
        unsigned long nowMs = millis();
        unsigned long dt = nowMs - lastBeatMs;

        if (dt > MIN_BEAT_INTERVAL && dt < MAX_BEAT_INTERVAL) {
          // Save interval into rolling buffer
          lastIntervals[ivIdx] = dt;
          ivIdx = (ivIdx + 1) % CONSIST_PEAKS;
          if (ivCount < CONSIST_PEAKS) ivCount++;

          // Check consistency: max and min interval within 25%
          bool consistent = true;
          if (ivCount == CONSIST_PEAKS) {
            unsigned long mn = lastIntervals[0], mx = lastIntervals[0];
            for (uint8_t i = 1; i < CONSIST_PEAKS; i++) {
              if (lastIntervals[i] < mn) mn = lastIntervals[i];
              if (lastIntervals[i] > mx) mx = lastIntervals[i];
            }
            consistent = (mx - mn) * 4 < mn; // difference < 25%
          }

          if (consistent) {
            bpm = (uint16_t)(60000UL / dt);
          }
          lastBeatMs = nowMs;
        } else if (dt >= MAX_BEAT_INTERVAL) {
          // Too long since last beat: reset timer but do not update BPM
          lastBeatMs = nowMs;
          ivCount = 0;
        }
      }
      above = nowAbove;
    } else {
      above = false;
    }

    // Reset BPM if no beat detected for too long
    if (millis() - lastBeatMs > BPM_TIMEOUT_MS) {
      bpm = 0;
      ivCount = 0;
    }

    // LED indicates threshold crossing
    digitalWrite(LED_PIN, (contact && above) ? HIGH : LOW);

    // Serial Plotter output: raw pulse and calculated BPM
    Serial.printf("pulse:%u\tvalue2:%u\n", pulse_reading, bpm);
    //>>>>> Insert code here so that each switch operates as a push on/push off switch rather than momentary contact
    // what is happening on this line?
    // if (switch1.update(digitalRead(SWITCH_PIN))) //check if the switch is being an
    // {
    // // Serial.printf("New switch state: ->%x\n", switch1.state());
    // // if (switch1.state())//only run the next line if the switch is toggled to true state (will not do anything if the switch is toggled off)
    // // {
    // // latching_1 = !latching_1; //changes switch boolean
    // // Serial.printf("Latching signal state -> %x\n", latching_1);
    // // }
    // }
    
    //************************************************************



    //*********************** 1 sec tasks *********************
    if (++tick1sec >= TICK_1SEC) {
      // execute 1 second tasks
      // Serial.printf("\nTICK1: %.3f microsec\n", micros()*1.);
      tick1sec = 0;

      secondsToD++;  // update time of day
    }
    //************************************************************



    //*********************** 10 sec tasks *********************
    // if (++tick10sec >= TICK_10SEC) {
    //   Serial.printf("\nTICK10: %.3f sec\n", millis()/1000.);
    //   calculatetime();
    //   Serial.printf("Time elapsed - %02d:%02d:%02d \n", hoursCounter, minutesCounter, secondsCounter);
      
    //   tick10sec = 0;
    // }
    //************************************************************

  } // 20 msec tick
}
