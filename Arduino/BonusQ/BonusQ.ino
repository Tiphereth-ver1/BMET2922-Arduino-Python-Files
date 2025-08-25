/*
 * Display information about the ESP32 module.
 * Introduce a number of print options.
 * 
 * Author:  Greg Watkins
 * Date:    July 2021
 * 
 * Modified by Daniel Babekuhl, 2023.
 */

// define the IO pin for the led
#define LED1 25  // IO32
#define LED2 26  // IO32
#define LED3 27  // IO32


// define the IO pin for the switch
#define SW1 35  // IO33

// loop time in milliseconds (see how it is used in the loop function below)
#define SEC_10 10000
#define SEC_5 5000
#define SEC_3 3000
#define SEC_1 1000
#define MSEC_100 100
#define MSEC_30 30
#define MSEC_50 50
#define MSEC_60 60

uint8_t i = 0;
uint8_t switchCount = 0;
bool state = true;


// function to print processor information
void printUcInfo(void) {

  // print a constant string terminated with an "end of line" char
  Serial.println("*******************");
  Serial.println("* ESP INFORMATION *");
  Serial.println("*******************");
  Serial.println();

  // print a string using a format string
  //  The string in quotes is a "format string"
  //  %s is substituted with a string parameter from getChipModel function
  //  %d is substituted with a decimal number fomr getChipRevision function
  //
  Serial.printf("ESP32\n");
  Serial.printf("      Model : %s\n", ESP.getChipModel());
  Serial.printf("        Rev : %4d\n", ESP.getChipRevision());
  Serial.printf("      Cores : %4d\n", ESP.getChipCores());

  char buf[128];
  //
  // alternatively, the string can be written into the variable buf and then printed.
  //
  sprintf(buf, "Clocks Xtal : %4d MHz", getXtalFrequencyMhz());
  Serial.println(buf);
  sprintf(buf, "       CPU  : %4d MHz", getCpuFrequencyMhz());
  Serial.println(buf);
  sprintf(buf, "       APB  : %4d MHz", getApbFrequency() / 1000000);
  Serial.println(buf);
  sprintf(buf, "Memory Flash: %4d kB", ESP.getFlashChipSize() / 1000);
  Serial.println(buf);
  sprintf(buf, "       PSRam: %4d kB", ESP.getPsramSize() / 1000);
  Serial.println(buf);
  sprintf(buf, "       Heap : %4d kB", ESP.getHeapSize() / 1000);
  Serial.println(buf);
  sprintf(buf, "Sketch Size : %4d kB", ESP.getSketchSize() / 1000);
  Serial.println(buf);
  sprintf(buf, "       Free : %4d kB", ESP.getFreeSketchSpace() / 1000);
  Serial.println(buf);
  Serial.println();
}

// void blink(int blinker) {
//   for (int j = 0; j < blinker; j ++)
//   digitalWrite(LED1,1);
//   delay(MSEC_30);
//   digitalWrite(LED,0);
//   delay(MSEC_30);
// }

bool holdstate(void) {
  unsigned long start = millis();
  bool toggle = true;
  Serial.println("Holdstate started");
  while (digitalRead(SW1)) {
    delay(MSEC_50);
  }
  unsigned long end = millis();
  Serial.println(end-start);
  if ((end - start) > SEC_3) {
    Serial.println("Sufficient length to activate LED 3.");
    return true;
  }
  Serial.println("Insufficient length to activate LED 3.");
  return false;
}

void lightswitch(int i) {
  if (i==1) {
        digitalWrite(LED1,1);
        digitalWrite(LED2,0);
        digitalWrite(LED3,0);
        Serial.println("LED 1 activated.");
  }
  else if (i==2) {
        digitalWrite(LED1,0);
        digitalWrite(LED2,1);
        digitalWrite(LED3,0);
        Serial.println("LED 2 activated.");
  }
  else if (i == 3) {
        digitalWrite(LED1,0);
        digitalWrite(LED2,0);
        digitalWrite(LED3,1);
        Serial.println("LED 3 activated.");
  }
}

bool secondpress() {
  unsigned long start = millis();
  unsigned long end = millis();
  while ((end - start) < 200) {
  if (digitalRead(SW1) != false) {
    switchCount++;
    Serial.println(switchCount);

    if (switchCount >= 5) {
      switchCount = 0;
      return true;
    }
    }
  else {
    if (switchCount > 1)
    switchCount--;
  }

  delay(20);
  end = millis();
  }
  return false;
}
// One setup function is required for all Arduino sketches. It runs once when you press reset or power the board
void setup() {


  // initialize LED pin as digital output. It can be High (3.3V) or low (0V)
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);


  // initialize switch pin as digital output. It can be High (1) or low (0)
  pinMode(SW1, INPUT);

  // set the state of the LED
  digitalWrite(LED1, 0);

  // start the Serial interface (over USB) that writes to the Serial Monitr at the specified bit rate
  Serial.begin(115200);
}

// One loop function is required for all Arduino sketches. It runs over and over again forever.
void loop() {

  if (digitalRead(SW1) != state) {
    switchCount++;
    Serial.println(switchCount);

    if (switchCount >= 5) {
      switchCount = 0;
      state = !state;
      if (state) {
        if (holdstate()) {lightswitch(3);}
      else if (secondpress()){
        lightswitch(2);
      }
      else {
        lightswitch(1);
        }
      }
    }
    }
  else {
    if (switchCount > 1)
    switchCount--;
  }

  delay(20);

}

