\# Arduino Robot Movement



\## Overview



This Arduino program controls the movement of the AI-powered Emotion Detection and Medication Reminder Robot. The Arduino Uno is responsible for real-time navigation, obstacle detection, and motor control, while the Raspberry Pi 4B performs AI-based emotion recognition and medication reminder tasks.



\---



\## Hardware Used



\- Arduino Uno

\- Adafruit Motor Shield (AFMotor Library)

\- 4 × DC Motors

\- HC-SR04 Ultrasonic Sensor

\- 2 × IR Obstacle Sensors

\- Robot Chassis

\- Raspberry Pi 4B (connected separately)



\---



\## Features



\- Forward movement using ultrasonic distance sensing.

\- Backward movement when both IR sensors detect obstacles.

\- Left and right turning for obstacle avoidance.

\- Automatic motor stopping when no movement condition is satisfied.

\- Continuous real-time sensor monitoring.



\---



\## Working Principle



1\. The ultrasonic sensor continuously measures the distance in front of the robot.

2\. The left and right IR sensors detect nearby obstacles.

3\. Based on sensor inputs, the Arduino decides whether to:

&#x20;  - Move Forward

&#x20;  - Move Backward

&#x20;  - Turn Left

&#x20;  - Turn Right

&#x20;  - Stop

4\. The Adafruit Motor Shield drives all four DC motors according to the selected action.

5\. The Raspberry Pi independently performs emotion recognition and communicates with the user through the display and speaker.



\---



\## Sensor Logic



| Sensor Condition | Robot Action |

|------------------|--------------|

| Distance ≤ 20 cm | Move Forward |

| Left IR triggered | Turn Right |

| Right IR triggered | Turn Left |

| Both IR triggered | Move Backward |

| No obstacle detected | Stop |



\---



\## Libraries Used



\- AFMotor

\- Arduino Core Libraries



\---



\## File



\- `robot\_movement.ino` – Arduino source code for robot navigation and obstacle avoidance.

