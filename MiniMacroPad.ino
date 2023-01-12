// MiniMacroPad

#define LED_PIN 17
#define BTN_1_PIN 5
#define BTN_2_PIN 7
#define BTN_3_PIN 9
#define BTN_4_PIN 8
#define _DELAY 150

void setup() {
  // pinMode(LED_PIN, OUTPUT);
  pinMode(BTN_1_PIN, INPUT_PULLUP);
  pinMode(BTN_2_PIN, INPUT_PULLUP);
  pinMode(BTN_3_PIN, INPUT_PULLUP);
  pinMode(BTN_4_PIN, INPUT_PULLUP);
  
  Serial.begin(9600);
}

void loop() {
  handleInput();
}

void handleInput() {
  
  if (digitalRead(BTN_1_PIN) == LOW) {
    Serial.println("1");
    delay(_DELAY);
  }
  if (digitalRead(BTN_2_PIN) == LOW) {
    Serial.println("2");
    delay(_DELAY);
  }
  if (digitalRead(BTN_3_PIN) == LOW) {
    Serial.println("3");
    delay(_DELAY);
  }
  if (digitalRead(BTN_4_PIN) == LOW) {
    Serial.println("4");
    delay(_DELAY);
  }
}

void blink() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}