# Machine Control & Monitoring with Unity and AI Chatbot

<img src="https://lauzhack.com/images/logo.svg" alt="logo" width="500"/>

![Hackathon](https://lauzhack.com/) EPFL Lausanne, Switzerland<br>
November 30 - December 1
---
## Authors
- Arnau Claramunt
- Genís López
- Jaume López
- Pay Mayench

[![GitHub followers](https://img.shields.io/github/followers/ArnauCS03?label=ArnauCS03)](https://github.com/ArnauCS03) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/GenisLopez5?label=GenisLopez5)](https://github.com/GenisLopez5) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/EncryptEx?label=EncryptEx)](https://github.com/EncryptEx) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/PauMayench?label=PauMayench)](https://github.com/PauMayench) <br><br>


---

## Project Overview

This project is the implementation of the **Bobst Company challenge** presented at the LauzHack24 Hackathon. We assembled a 3D printed conveyor belt machine, represent the virtual model in Unity and use a chatbot with a small LLM to also interact with the machine.

**Key Features**:  
- **3D-Printed Conveyor Belt** controlled by a Raspberry Pi.  
- Real-time data collection (speed, box counter, energy usage).  
- AI-powered chatbot for troubleshooting and monitoring via **Ollama's Llama 3.2**.  
- Interactive HMI built in **Unity** for real-time control and visualization.  
- Dockerized architecture for easy deployment.
- Bridge between Unity and Ollama with FastAPI.


---

## 🛠️ Technologies & Tools  

| **Component**       | **Technology**    | **Purpose**                                   |
|----------------------|-------------------|-----------------------------------------------|
| **Hardware**         | Raspberry Pi      | Controls conveyor belt and collects metrics. |
| **Modeling**         | Unity             | Creates a 3D visualization of the machine.   |
| **API Layer**        | FastAPI           | Communication between AI and Unity and Unity to Raspberry Pi.  |
| **AI**               | Ollama (Llama 3.2)| Context-aware troubleshooting LLM chatbot.   |
| **Deployment**       | Docker            | Simplified deployment of all components.     |

---

## Bob the AI Chatbot  


<img src="https://github.com/user-attachments/assets/aa974f4d-28fc-481a-b16a-9a7cf045e1f4" width="200"/>

Meet **Bob**, our AI-powered assistant built on **Ollama's Llama 3.2**. Bob is integrated into the system, providing real-time assistance, troubleshooting, and even direct control over the conveyor belt.

---

### 🧠 How Bob Works  

1. **Understand Context**:  
   Bob uses the machine's current state (e.g., motor status, speed, output metrics) as context for user interactions.

2. **Interpret User Queries**:  
   Natural language queries are passed to Bob along with the machine state for precise and actionable responses.

3. **Execute Actions**:  
   When appropriate, Bob translates its recommendations into **machine actions** via API calls to the Unity that then calls the Raspberry Pi.


<br>


## 🔮 Future Improvements
- Add more sensors for enhanced data insights.
- Introduce predictive maintenance using AI.
- Expand HMI with detailed production analytics.

<br>

---

### Screenshots

Conveyor belt machine:
![IMG20241201111510](https://github.com/user-attachments/assets/a1c6302c-2a39-4ec9-8342-4851ba1c60b9)


The machine operates with a safety feature that performs a secure stop to prevent accidents when a hand is detected near the belt:


https://github.com/user-attachments/assets/0fd7f19d-bdc7-44b0-82ea-ef1dd0de94f4



Unity interface:
![Captura_5](https://github.com/user-attachments/assets/ef5957ea-d579-46e6-9464-a22fba821c0b)
![aimage](https://github.com/user-attachments/assets/7947538a-e56b-42aa-b0e9-361fe7e13a50)


API for talking to the Raspberry Pi 5:
![Screenshot from 2024-12-01 04-36-22](https://github.com/user-attachments/assets/71442875-a2fd-4d2d-a9a7-f798587fd7a7)



<br>

---

### Setup instructions

1. Clone the Repository:  
```bash
git clone git@github.com:EncryptEx/machine-control-monitoring.git
cd machine-control-monitoring
```

2. Build and run Dockers containers: (form the `chatbot_api` folder)
```bash
docker-compose up --build
```

3. Launch Unity Application:<br>
Open the Unity project in your IDE and run the scene.

4. Interact with Bob:<br>
Use the chatbot interface in Unity to troubleshoot and control the conveyor.


<br><br>
