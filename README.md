ASTRA - Adaptive System for Touchless Response & Accessibility

Description:
ASTRA is an intelligent interface that enables touchless control of your computer using hand gestures and eye movements.  
It provides an intuitive and accessible way to interact without the need for physical input devices,  
combining gesture recognition and gaze tracking into a seamless user experience.

Modes:
- H.A.N.D.S (Human Actuated Navigation & Dynamic System):  
  Navigate, click, scroll, and control applications using hand gestures.

- I.R.I.S (Intelligent Retinal Interaction System):  
  Control the cursor, perform clicks, and open applications using eye movements and blinks.

Features:
- Adaptive interaction system with low false trigger rate.
- Simple mode selection interface with futuristic HUD design.

Installation:
1. Install Python 3.12 or later.
2. Install dependencies:
   pip install -r requirements.txt

Usage:
1. Run main.py
   python main.py
2. Choose mode:
   [H] HANDS – Hand Gesture Mode  
   [G] IRIS  – Eye/Gaze Tracking Mode  
   [Q] Quit
3. Follow on-screen instructions.

Requirements:
- Python 3.12+
- OpenCV
- Mediapipe
- PyAutoGUI
- Pycaw

Folder Structure:
├── main.py       # Entry point and menu  
├── hands.py      # Hand mode implementation  
├── iris.py       # Eye mode implementation  
├── requirements.txt  
├── README.md

License:
MIT License

Author:
Ishanya Tripathi
