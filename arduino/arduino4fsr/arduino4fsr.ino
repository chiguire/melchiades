#define FSR0 A0
#define FSR1 A1
#define FSR2 A2
#define FSR3 A3
#define FSRN 4

int fsrs[] = {FSR0, FSR1, FSR2, FSR3};
int vMin[] = {1023, 1023, 1023, 1023};
int vMax[] = {0,    0,    0,    0};
int vals[] = {0,0,0,0};

int echoPin = 9;
int trigPin = 10;
int ledPin = 8;

#define DISTSN 9
#define DIST_TRIGGER 400
int dists[DISTSN];
int distsIndex;

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i != FSRN; i++)
  {
    pinMode (fsrs[i], INPUT);
  }
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  memset(dists, 0, DISTSN);
  Serial.begin (9600);
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
  // fsr buttons
  for (int i = 0; i != FSRN; i++)
  {
    int v = analogRead(fsrs[i]);
    v = map (v, vMin[i], vMax[i], 0, 255);
    v = constrain(v, 0, 255);
    vals[i] = v;
  }

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
  
  Serial.print(vals[0]);Serial.print(',');
  Serial.print(vals[1]);Serial.print(',');
  Serial.print(vals[2]);Serial.print(',');
  Serial.print(vals[3]);Serial.print(',');
  Serial.println(resultdistance);
  
  delay (50);
}
 

