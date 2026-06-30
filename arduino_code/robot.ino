#include <AFMotor.h>

// Motors: M1–M4 on motor shield
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

// Sensor pins
#define trigPin A4
#define echoPin A5
#define irLeftPin A2
#define irRightPin A3

// Distance threshold (cm) for forward operation
const int FORWARD_DISTANCE_CM = 20;

// Motor speeds
const uint8_t FORWARD_SPEED = 130;
const uint8_t TURN_SPEED    = 130;
const uint8_t BACK_SPEED    = 120;

void setup() {
  Serial.begin(9600);

  // Set initial motor speeds
  motor1.setSpeed(FORWARD_SPEED);
  motor2.setSpeed(FORWARD_SPEED);
  motor3.setSpeed(FORWARD_SPEED);
  motor4.setSpeed(FORWARD_SPEED);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(irLeftPin, INPUT);
  pinMode(irRightPin, INPUT);
}

void loop() {
  int distance = getDistance();

  // IR assumed active LOW (LOW = object detected)
  bool leftDetected  = (digitalRead(irLeftPin) == LOW);
  bool rightDetected = (digitalRead(irRightPin) == LOW);

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" cm, IR Left: ");
  Serial.print(leftDetected);
  Serial.print(", IR Right: ");
  Serial.println(rightDetected);

  // Priority logic:
  // 1) If BOTH IR sensors triggered -> move BACKWARD (continuous)
  //    and continue moving backward until BOTH IR become untriggered.
  // 2) If single IR -> turn (unchanged behavior, those functions use delay(600))
  // 3) Else if distance <= FORWARD_DISTANCE_CM -> move FORWARD (continuous)
  // 4) Else -> STOP

  if (leftDetected && rightDetected) {
    // BOTH IR triggered -> move backward continuously
    moveBackward();
  }
  else if (leftDetected && !rightDetected) {
    // Object on left -> pivot/turn right (blocking 600ms as before)
    turnRight();
  }
  else if (rightDetected && !leftDetected) {
    // Object on right -> pivot/turn left (blocking 600ms as before)
    turnLeft();
  }
  else if (distance <= FORWARD_DISTANCE_CM) {
    // Object within forward range -> move forward continuously
    moveForward();
  }
  else {
    // No relevant trigger -> stop
    stopMotors();
  }

  // No delay here so the loop responds quickly to sensor changes.
}

// Ultrasonic distance measurement (cm)
int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);  // timeout 30 ms
  if (duration == 0) return 999; // treat as far

  return (int)(duration * 0.034 / 2);
}

void moveForward() {
  motor1.setSpeed(FORWARD_SPEED);
  motor2.setSpeed(FORWARD_SPEED);
  motor3.setSpeed(FORWARD_SPEED);
  motor4.setSpeed(FORWARD_SPEED);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void moveBackward() {
  motor1.setSpeed(BACK_SPEED);
  motor2.setSpeed(BACK_SPEED);
  motor3.setSpeed(BACK_SPEED);
  motor4.setSpeed(BACK_SPEED);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void turnLeft() {
  motor1.setSpeed(TURN_SPEED);
  motor2.setSpeed(TURN_SPEED);
  motor3.setSpeed(TURN_SPEED);
  motor4.setSpeed(TURN_SPEED);

  // Pivot left: left wheels backward, right wheels forward
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
  delay(600);
  stopMotors();
}

void turnRight() {
  motor1.setSpeed(TURN_SPEED);
  motor2.setSpeed(TURN_SPEED);
  motor3.setSpeed(TURN_SPEED);
  motor4.setSpeed(TURN_SPEED);

  // Pivot right: left wheels forward, right wheels backward
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
  delay(600);
  stopMotors();
}

void stopMotors() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}