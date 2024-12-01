# LauzHack24

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
- Integration with **Azure IoT Hub** for seamless monitoring.  
- AI-powered chatbot for troubleshooting and monitoring via **Ollama's Llama 3.2**.  
- Interactive HMI built in **Unity** for real-time control and visualization.  
- Dockerized architecture for easy deployment.
- Bridge between Unity and Ollama with FastAPI


---

## 🛠️ Technologies & Tools  

| **Component**       | **Technology**    | **Purpose**                                   |
|----------------------|-------------------|-----------------------------------------------|
| **Hardware**         | Raspberry Pi      | Controls conveyor belt and collects metrics. |
| **Modeling**         | Unity             | Creates a 3D visualization of the machine.   |
| **API Layer**        | FastAPI           | Communication between Unity and AI.          |
| **AI**               | Ollama (Llama 3.2)| Context-aware troubleshooting chatbot.       |
| **IoT**              | Azure IoT Hub     | Centralized data collection and monitoring.  |
| **Deployment**       | Docker            | Simplified deployment of all components.     |

---


## 🔮 Future Improvements
- Add more sensors for enhanced data insights.
- Introduce predictive maintenance using AI.
- Expand HMI with detailed production analytics.

<br><br>
### Screenshots

Conveyor belt machine:


API for talking to the Raspberry Pi 5:
![Screenshot from 2024-12-01 04-36-22](https://github.com/user-attachments/assets/71442875-a2fd-4d2d-a9a7-f798587fd7a7)




<br><br>

---

### Clone the Repository:  
```bash
git clone https://github.com/yourusername/lauzhack24.git
cd lauzhack24
```


<br><br>
