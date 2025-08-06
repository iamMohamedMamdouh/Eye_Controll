# 👁 Eye-Controlled Japanese Virtual Keyboard 🇯🇵

## This is an AI-powered assistive technology project that allows users to control the mouse with their eyes and type Japanese characters using a virtual keyboard — with real-time Arabic translation and Japanese speech synthesis. It's designed with accessibility in mind, especially for users with motor disabilities or for use in hands-free environments.


## 🧠 Features

👁 Eye-controlled mouse pointer using MediaPipe FaceMesh.

🖱 Click by blinking (left or right eye configurable).

⌨ On-screen Japanese Hiragana keyboard built with Tkinter.

🔁 Live Arabic translation using Google Translate API.

🔊 Japanese speech output with gTTS and pygame.

🗑 Clear all / ⌫ Delete last character buttons.

🧩 Multithreaded: Keyboard runs independently from eye tracker.



## 📸 How it works

Camera captures the user's face in real-time.
Mediapipe detects facial landmarks to determine eye movement and blinks.
PyAutoGUI controls the mouse pointer.
Tkinter GUI shows a clickable Japanese keyboard.
Selected text is translated and spoken using Google Text-to-Speech.


## 🛠 Tech Stack

Python 3.9+
OpenCV
MediaPipe
Tkinter
gTTS
pygame
pyautogui
deep_translator



## 🧪 How to Run

1. Install dependencies:
   
pip install opencv-python mediapipe pyautogui pygame gtts deep_translator

2. Run the app:

python keyboard_control.py

# > 📝 Make sure your webcam is connected and working.



## 🧑‍💻 Use Cases

Assistive technology for people with limited mobility.
Language learning for Japanese with real-time pronunciation and translation.
Human-computer interaction experiments.


## 📌 Known Limitations

May experience latency depending on CPU.
Accuracy of eye tracking depends on lighting and camera angle.
No full text prediction yet — limited to character-by-character input.


## 📜 License
This project is open-source under the MIT License.


## 🤝 Contribute

Feel free to fork the repo, open issues, or suggest features
🤝 Contribute

Feel free to fork the repo, open issues, or suggest features!
