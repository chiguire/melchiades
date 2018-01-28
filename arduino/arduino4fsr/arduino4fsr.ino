#define FSR0 A0
#define FSR1 A1
#define FSR2 A2
#define FSR3 A3
#define FSRN 4

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#include <Servo.h>

#define NEOPIXEL0PIN 34
#define NEOPIXEL1PIN 32
Adafruit_NeoPixel strip0 = Adafruit_NeoPixel(3, NEOPIXEL0PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip1 = Adafruit_NeoPixel(7, NEOPIXEL1PIN, NEO_GRB + NEO_KHZ800);

int fsrs[] = {FSR0, FSR1, FSR2, FSR3};
int vMin[] = {1023, 1023, 1023, 1023};
int vMax[] = {0,    0,    0,    0};
int vals[] = {0,0,0,0};

int echoPin = 9;
int trigPin = 10;
int ledPin = 8;
int servo0Pin = 11;

int blinky0Pin = 7;
int blinky1Pin = 6;
int blinky2Pin = 22;//24 26 28 30
int blinky3Pin = 24;
int blinky4Pin = 26;
int blinky5Pin = 28;
int blinky6Pin = 30;


int blinky0Timer = 0;
int blinky1Timer = 0;
#define BLINKY_TARGET_TIMER 256
#define BLINKY_ON_TIMER 128

#define DISTSN 5
#define DIST_TRIGGER 200
int dists[DISTSN];
int distsIndex;

#define SERVO_SPEED 5
int servo0Angle = 60;
int servo0Min = 60;
int servo0Max = 140;
int servo0Dir = SERVO_SPEED;
int servo0Angles[] = { 60, 80, 100, 120, 140, 0 };
int servo0Index = 5;
int servo0RequestedIndex = 5;

Servo servo0;

int rainbowI = 0;

long melchiadesWorking = 0;

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i != FSRN; i++)
  {
    pinMode (fsrs[i], INPUT);
  }
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(blinky0Pin, OUTPUT);
  pinMode(blinky1Pin, OUTPUT);
  pinMode(blinky2Pin, OUTPUT);
  pinMode(blinky3Pin, OUTPUT);
  pinMode(blinky4Pin, OUTPUT);
  pinMode(blinky5Pin, OUTPUT);
  pinMode(blinky6Pin, OUTPUT);
  blinky0Timer = 0;
  blinky1Timer = 0;
  servo0.attach(servo0Pin);
  servo0.write(servo0Angles[5]);
  memset(dists, 0, DISTSN);
  strip0.begin();
  strip0.show(); // Initialize all pixels to 'off'
  strip1.begin();
  strip1.show(); // Initialize all pixels to 'off'
  Serial.begin (9600);
  Serial.println("Calibrate!");
  Serial.setTimeout(25);
  while (millis() < 5000) {
    for (int i = 0; i != FSRN; i++)
    {
      int v = analogRead(fsrs[i]);
      if (v > vMax)
      {
        vMax[i] = v;
      }
      if (v < vMin)
      {
        vMin[i] = v;
      }
    }
  }
}


void loop() {
  // distance sensor
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  int distance = duration*0.034/2;

  dists[distsIndex] = distance;
  distsIndex = (distsIndex + 1) % DISTSN;
  
  // Averaging distance
  long d = 0;
  for (int i = 0; i != DISTSN; i++)
  {
    d += dists[i];
  }
  float resultdistance = d / DISTSN;

  if (resultdistance > DIST_TRIGGER)
  {
    digitalWrite(ledPin, HIGH);
  }
  else
  {
    digitalWrite(ledPin, LOW);
  }

  long commandFrom = Serial.parseInt();

  if (commandFrom == 1)
  {
    melchiadesWorking = 0;
    servo0RequestedIndex = 5;

    if (servo0Index != servo0RequestedIndex)
    {
      servo0.write(servo0Angles[servo0RequestedIndex]);
      servo0Index = servo0RequestedIndex;
    }

    neopixelClear();
  }
  else if (commandFrom == 2)
  {
    melchiadesWorking = 1;

    long idx = random(0, 5);
    servo0RequestedIndex = idx;
    
    if (servo0Index != servo0RequestedIndex)
    {
      servo0.write(servo0Angles[servo0RequestedIndex]);
      servo0Index = servo0RequestedIndex;
    }
  }

  if (melchiadesWorking == 0)
  {
    // fsr buttons
    for (int i = 0; i != FSRN; i++)
    {
      int v = analogRead(fsrs[i]);
      v = map (v, vMin[i], vMax[i], 0, 255);
      v = constrain(v, 0, 255);
      vals[i] = v;
    }

    digitalWrite(blinky0Pin, LOW);
    digitalWrite(blinky1Pin, LOW);
    digitalWrite(blinky2Pin, LOW);
    digitalWrite(blinky3Pin, LOW);
    digitalWrite(blinky4Pin, LOW);
    digitalWrite(blinky5Pin, LOW);
    digitalWrite(blinky6Pin, LOW);
  }
  else 
  {
    //Servo 0 sweep
    //if (servo0Dir < 0 && servo0Angle <= servo0Min)
    //{
    //  servo0Dir = SERVO_SPEED;
    //  servo0Angle = servo0Min;
    //}
    //else if (servo0Dir > 0 && servo0Angle >= servo0Max)
    //{
    //  servo0Dir = -SERVO_SPEED;
    //  servo0Angle = servo0Max;
    //}
    //servo0Angle += servo0Dir;
    //servo0.write(servo0Angle);
  
    blinky0Timer = (blinky0Timer + 1) % BLINKY_TARGET_TIMER;
    blinky1Timer = (blinky1Timer + 1) % BLINKY_TARGET_TIMER;
  
    digitalWrite(blinky0Pin, (blinky0Timer > BLINKY_ON_TIMER? HIGH: LOW));
    digitalWrite(blinky1Pin, (blinky1Timer > BLINKY_ON_TIMER? HIGH: LOW));
    digitalWrite(blinky2Pin, (blinky1Timer > BLINKY_ON_TIMER? LOW: HIGH));
    digitalWrite(blinky3Pin, (blinky1Timer > BLINKY_ON_TIMER? HIGH: LOW));
    digitalWrite(blinky4Pin, (blinky1Timer > BLINKY_ON_TIMER? LOW: HIGH));
    digitalWrite(blinky5Pin, (blinky1Timer > BLINKY_ON_TIMER? HIGH: LOW));
    digitalWrite(blinky6Pin, (blinky1Timer > BLINKY_ON_TIMER? LOW: HIGH));
    
    rainbowI = (rainbowI + 1) % 256;
    rainbowCycle(rainbowI);
  }
  
  //Print values from sensors
  
  Serial.print(vals[0]);Serial.print(',');
  Serial.print(vals[1]);Serial.print(',');
  Serial.print(vals[2]);Serial.print(',');
  Serial.print(vals[3]);Serial.print(',');
  Serial.print(resultdistance);Serial.print(',');
  Serial.println(melchiadesWorking);
  
  delay (50);
}

void neopixelClear() {
  int i;
  for(i=0; i< strip0.numPixels(); i++) {
    strip0.setPixelColor(i, strip0.Color(0,0,0));
  }
  strip0.show();

  for(i=0; i< strip1.numPixels(); i++) {
    strip1.setPixelColor(i, strip1.Color(0,0,0));
  }
  strip1.show();
}
// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(int j) {
  int i;
  for(i=0; i< strip0.numPixels(); i++) {
    strip0.setPixelColor(i, Wheel(((i * 256 / strip1.numPixels()) + j) & 255));
  }
  strip0.show();

  for(i=0; i< strip1.numPixels(); i++) {
    strip1.setPixelColor(i, Wheel(((i * 256 / strip1.numPixels()) + j) & 255));
  }
  strip1.show();
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip0.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip0.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip0.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
