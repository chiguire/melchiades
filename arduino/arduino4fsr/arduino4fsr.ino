#define FSR0 A0
#define FSR1 A1
#define FSR2 A2
#define FSR3 A3
#define FSRN 4

int fsrs[] = {FSR0, FSR1, FSR2, FSR3};
int vMin[] = {1023, 1023, 1023, 1023};
int vMax[] = {0,    0,    0,    0};
int vals[] = {0,0,0,0};

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i != FSRN; i++)
  {
    pinMode (fsrs[i], INPUT);
  }
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
  // put your main code here, to run repeatedly:
  for (int i = 0; i != FSRN; i++)
  {
    int v = analogRead(fsrs[i]);
    v = map (v, vMin[i], vMax[i], 0, 255);
    v = constrain(v, 0, 255);
    vals[i] = v;
  }
  Serial.print(vals[0]);Serial.print(',');
  Serial.print(vals[1]);Serial.print(',');
  Serial.print(vals[2]);Serial.print(',');
  Serial.println(vals[3]);
  
  delay (50);
}
 

