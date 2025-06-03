# Reflect AI - A Smart Mirror

Reflect AI is a smart mirror system that displays real-time weather, news, date/time, and personalized info using a Raspberry Pi. Built to enhance daily routines with quick, interactive updates.

---

### ✅ Features

- Voice-controlled smart mirror using speech recognition.
- AI-powered responses via Google Gemini API.
- Real-time weather, date, and time display.
- Fullscreen graphical interface with Pygame.
- Handles voice commands including exit to quit interface.

---

### 🖼️ Demo

[Watch the demo video](https://drive.google.com/file/d/1-1IoBSU_Me0rmJPWWyJdY9lx7j7Qhgse/view?usp=sharing)
![Smart Mirror Screenshot](images/display-showing-date,time,weather,and-AI-response.png)
![Smart Mirror Screenshot](images/Query-displayed-on-the-two-way-mirror.png)
![Smart Mirror Screenshot](images/Gemini-response-on-mirror-display.png)

---

### 💻 Technologies Used

- Python, Pygame(GUI)
- Voice Processing Libraries : SpeechRecognition, PyAudio
- APIs: Google Generative AI API Key, OpenWeatherMap API Key
- Hardware: Raspberry Pi 3B+, USB Microphone, Monitor, Two-Way Mirror
- 
---

### ⚙️ Installation

```bash
git clone https://github.com/yourusername/reflect-ai.git
cd reflect-ai
pip install -r requirements.txt
python app.py
