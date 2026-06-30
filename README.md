# 🤖 AI-Powered Emotional Companion & Smart Medication Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Gesture%20Recognition-red)
![Ollama](https://img.shields.io/badge/Ollama-Phi--3-purple)
![Arduino](https://img.shields.io/badge/Arduino-Uno-blue)
![Raspberry%20Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-C51A4A)
![Twilio](https://img.shields.io/badge/Twilio-SMS-red)

---

# 📖 Project Overview

The **AI-Powered Emotional Companion & Smart Medication Assistant** is an intelligent healthcare assistance robot developed to provide emotional support and improve medication adherence for elderly people, patients, and individuals requiring continuous care.

The system combines **Artificial Intelligence, Computer Vision, Embedded Systems, Robotics, and IoT** technologies into a single smart assistant capable of understanding a patient's emotional condition, engaging in supportive conversations, reminding users to take medicines, verifying medicine intake through gesture recognition, and notifying caregivers whenever medication is missed.

The project is built around a **Raspberry Pi 4B**, which performs AI inference and manages communication between all software modules, while an **Arduino Uno** independently controls the robot's movement and obstacle avoidance.

Emotion recognition is implemented using **TensorFlow** and **OpenCV**, gesture recognition is performed using **MediaPipe**, conversational AI is powered by the **Phi-3 Large Language Model** running locally through **Ollama**, and **Twilio Cloud Messaging** is used for caregiver notifications.

This project demonstrates the integration of Edge AI, Robotics, Embedded Systems, Computer Vision, and Large Language Models into a real-world healthcare application.

---

# 🌟 Key Features

## 😊 AI Emotion Recognition

- Real-time facial emotion detection
- CNN-based deep learning model
- Seven emotion classification
- Live webcam monitoring
- Emotion confidence prediction

---

## 🤖 AI Emotional Companion

- Conversational AI using Ollama
- Phi-3 Large Language Model
- Emotion-aware conversations
- Context-based supportive responses
- Local AI execution

---

## 💊 Smart Medication Reminder

- RTC-based medication scheduling
- Automatic reminder notifications
- Voice reminders
- Display notifications
- Scheduled medicine tracking

---

## ✋ Gesture Recognition

- MediaPipe hand tracking
- Touch-free medicine confirmation
- Real-time gesture detection
- Medication intake verification

---

## 📱 Caregiver Notification

- Twilio SMS integration
- Automatic alert generation
- Missed medication notification
- Remote caregiver communication

---

## 🚗 Autonomous Robot Navigation

- Arduino-based movement
- Obstacle avoidance
- Ultrasonic sensing
- IR sensor navigation
- Autonomous motion control

---

## 🛠 Hardware Components

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 4B | Main AI Processing Unit |
| Arduino Uno | Robot Navigation Controller |
| Camera Module | Emotion Detection |
| Microphone | Voice Input |
| Speaker / DFPlayer Mini | Voice Output |
| RTC Module | Medication Scheduling |
| Capacitive Touch Sensor | User Interaction |
| Ultrasonic Sensor (HC-SR04) | Distance Measurement |
| IR Sensors | Obstacle Detection |
| Adafruit Motor Shield | DC Motor Driver |
| 4 DC Motors | Robot Movement |
| LCD Display | User Interface |
| Robot Chassis | Mobile Platform |

---

# 💻 Software & Technologies

## Programming Languages

- Python
- C++
- JavaScript
- HTML
- CSS

---

## Artificial Intelligence

- TensorFlow
- Convolutional Neural Network (CNN)
- Ollama
- Phi-3 Large Language Model

---

## Computer Vision

- OpenCV
- MediaPipe

---

## Backend

- Flask
- Flask-CORS

---

## Frontend

- React
- Vite
- Axios

---

## Cloud Services

- Twilio API

---

## Development Tools

- VS Code
- Arduino IDE
- Git
- GitHub

---

## Python Libraries

- TensorFlow
- OpenCV
- MediaPipe
- NumPy
- Pandas
- Scikit-Learn
- Flask
- Flask-CORS

---

# 📂 Complete Project Structure

```text
Emotion_Detection/
│
├── arduino_code/
│   ├── robot_movement.ino
│   └── README.md
│
├── backend/
│   ├── app.py
│   ├── analyze_dataset.py
│   ├── evaluate_models.py
│   ├── test_models.py
│   ├── train.py
│   ├── requirements.txt
│   └── ...
│
├── datasets/
│   └── dataset_link.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   ├── index.css
│   └── ...
│
├── models/
│   ├── best-emotion-model.h5
│   └── train-model.h5
│
├── ollama_bridge/
│   ├── ollama_server.py
│   ├── requirements.txt
│   └── README.md
│
├── results/
│   ├── Emotion_Detection_Output.png
│   ├── Medication_Reminder.png
│   ├── Notification.png
│   └── Ollama_Server.png
│
├── robot/
│   ├── Robot_Prototype.jpg
│   ├── System_Architecture.png
│   ├── Block_Diagram.png
│   └── Hardware_Setup.png
│
├── .gitignore
└── README.md
```

# 🚀 Installation & Setup

## Prerequisites

Before running the project, ensure the following software and hardware are available.

### Software Requirements

- Python 3.11+
- Node.js 18+
- Git
- Arduino IDE
- Ollama
- Visual Studio Code

### Hardware Requirements

- Raspberry Pi 4B
- Arduino Uno
- USB Camera Module
- Microphone
- Speaker / DFPlayer Mini
- RTC Module
- Ultrasonic Sensor (HC-SR04)
- IR Sensors
- Adafruit Motor Shield
- Robot Chassis

---

# 📦 Project Setup

Clone the repository

```bash
git clone https://github.com/your-username/Emotion_Detection.git

cd Emotion_Detection
```

---

# 🧠 Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Raspberry Pi

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the Flask backend.

```bash
python app.py
```

The backend server starts at

```
http://localhost:5000
```

---

# 🌐 Frontend Setup

Navigate to the frontend folder.

```bash
cd frontend
```

Install all required packages.

```bash
npm install
```

Run the frontend.

```bash
npm run dev
```

The application will start at

```
http://localhost:5173
```

---

# 🤖 Ollama Bridge (Phi-3)

The project uses a locally hosted **Phi-3 Large Language Model** through **Ollama** for generating emotionally supportive conversational responses.

Instead of directly communicating with Ollama, the Raspberry Pi interacts with a Flask bridge server (`ollama_server.py`) that forwards prompts to the local Ollama instance and returns AI-generated responses.

## Ollama Bridge Setup

Navigate to the Ollama bridge folder.

```bash
cd ollama_bridge
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Ensure Ollama is installed and the Phi-3 model is available.

```bash
ollama pull phi3
```

Start the Ollama bridge server.

```bash
python ollama_server.py
```

The Flask bridge will run on

```
http://localhost:5000
```

---

## Ollama Workflow

```
Patient Voice
      │
      ▼
Microphone
      │
      ▼
Speech-to-Text
      │
      ▼
Flask Bridge (ollama_server.py)
      │
      ▼
Ollama (Phi-3)
      │
      ▼
Supportive AI Response
      │
      ▼
Speaker
```

---

## Features of Ollama Integration

- Local execution of Phi-3 Large Language Model
- Privacy-preserving conversational AI
- Emotion-aware supportive conversations
- Fast response generation
- Flask REST API integration
- Easy model replacement with other Ollama models

---

# 🚗 Arduino Navigation

Robot movement is independently controlled by an **Arduino Uno** using an **Adafruit Motor Shield**.

The Arduino continuously monitors sensor inputs and performs obstacle avoidance without interrupting the Raspberry Pi AI processes.

---

## Components Used

- Arduino Uno
- Adafruit Motor Shield
- HC-SR04 Ultrasonic Sensor
- Left IR Sensor
- Right IR Sensor
- Four DC Motors

---

## Navigation Features

- Autonomous Forward Movement
- Autonomous Backward Movement
- Left Turn
- Right Turn
- Obstacle Avoidance
- Continuous Sensor Monitoring
- Motor Speed Control

---

## Robot Navigation Logic

| Sensor Condition | Robot Action |
|------------------|--------------|
| Distance ≤ 20 cm | Move Forward |
| Left IR detects obstacle | Turn Right |
| Right IR detects obstacle | Turn Left |
| Both IR sensors detect obstacle | Move Backward |
| No obstacle detected | Stop |

---

## Navigation Workflow

```
Ultrasonic Sensor
        │
        ▼
Measure Distance
        │
        ▼
Read Left IR Sensor
        │
        ▼
Read Right IR Sensor
        │
        ▼
Arduino Decision Logic
        │
 ┌──────┼────────┬────────┬─────────┐
 ▼      ▼        ▼        ▼
Forward Left    Right   Backward
 Turn     Turn
        │
        ▼
 Stop (if no valid condition)
```

---

## Arduino Source Code

The complete Arduino navigation program is available inside:

```
arduino_code/
└── robot_movement.ino
```

The program performs:

- Obstacle detection
- Motor control
- Distance measurement
- Autonomous navigation
- Sensor monitoring
- Movement control

---

# 🔄 Overall Project Workflow

```
                  Camera
                     │
                     ▼
            Emotion Detection
          (TensorFlow + OpenCV)
                     │
                     ▼
            Emotion Classification
                     │
     ┌───────────────┴────────────────┐
     ▼                                ▼
Ollama (Phi-3)                 Medication Reminder
     │                                │
     ▼                                ▼
Supportive Response          RTC Scheduling
     │                                │
     ▼                                ▼
 Speaker                    Gesture Verification
                                      │
                                      ▼
                           Twilio SMS Notification
                                      │
                                      ▼
                                  Caregiver

Arduino Uno (Runs in Parallel)

IR Sensors + Ultrasonic Sensor
            │
            ▼
Obstacle Detection
            │
            ▼
Robot Navigation
```

# 📊 AI Model Details

The emotion recognition system is built using a **Convolutional Neural Network (CNN)** trained on the **FER2013** facial expression dataset.

## Model Architecture

- Convolutional Neural Network (CNN)
- TensorFlow Deep Learning Framework
- OpenCV for image preprocessing
- Softmax classifier for emotion prediction

---

## Emotion Classes

The model predicts the following seven human emotions:

- 😠 Angry
- 🤢 Disgust
- 😨 Fear
- 😊 Happy
- 😢 Sad
- 😮 Surprise
- 😐 Neutral

---

## Training Details

- Dataset: FER2013
- Image Size: 48 × 48 (Grayscale)
- Framework: TensorFlow
- Optimizer: Adam
- Loss Function: Categorical Cross Entropy
- Model Format: `.h5`

---

# 📂 Dataset

The project uses the **FER2013 Facial Expression Dataset** for training the CNN model.

For licensing reasons, the dataset is **not included** in this repository.

Download the dataset using the link provided in:

```
datasets/
└── dataset_link.txt
```

After downloading, place the dataset inside the appropriate training directory before retraining the model.

---

# 📷 Project Results

The `results` folder contains screenshots demonstrating the functionality of the complete system.

Available outputs include:

- Emotion Detection Output
- Medication Reminder
- Caregiver Notification
- Ollama Server Output

```
results/
│
├── Emotion_Detection_Output.png
├── Medication_Reminder.png
├── Notification.png
└── Ollama_Server.png
```

---

# 🤖 Robot Prototype

The `robot` folder contains the hardware design and implementation details of the robot.

Contents include:

- Robot Prototype Image
- System Architecture
- Block Diagram
- Hardware Setup

```
robot/
│
├── Robot_Prototype.jpg
├── System_Architecture.png
├── Block_Diagram.png
└── Hardware_Setup.png
```

---

# 🎯 Future Improvements

The project can be further enhanced with the following features:

- Voice biometrics for personalized interaction
- Health monitoring sensors (Heart Rate, SpO₂, Temperature)
- Cloud-based patient monitoring dashboard
- Mobile application support
- Multi-language voice interaction
- Face recognition for multiple users
- Emergency SOS detection
- Integration with hospital management systems
- AI-based health report generation
- Remote monitoring through IoT platforms

---

# 📁 Repository Highlights

This repository contains:

- Backend Source Code
- Frontend Source Code
- Arduino Navigation Code
- Ollama Bridge
- TensorFlow Training Scripts
- Trained CNN Models
- Dataset Download Link
- Robot Prototype Images
- Block Diagram
- System Architecture
- Project Results
- Documentation

---

# 🤝 Contributors

This project was developed as a collaborative academic project.

- Darshan N S  
  GitHub: https://github.com/bangre-16

- Lohith Arasu

- N Likhith  
  GitHub: https://github.com/likipersonal07-lgtm

- Sai Sidharth Pradhan
  GitHub: https://github.com/saisidharth4321-rgb

  
Department of Electrical and Electronics Engineering
Dayananda Sagar Academy of Technology and Management
Bengaluru, Karnataka, India

---

# 📄 License

This project is developed for **academic and educational purposes**.

Feel free to use this repository for learning and research with proper attribution.
