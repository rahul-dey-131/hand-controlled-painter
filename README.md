# 🖐️ Hand-Controlled Painter 🎨

**Draw, erase, and control brush size — all with your hand gestures. No mouse. No touchscreen. Just a webcam and your fingers.**

---

## 📌 Overview

**Hand-Controlled Painter** is an interactive, touchless painting application built with **OpenCV**, **MediaPipe**, and **Python**. It utilizes your **webcam feed** to detect hand landmarks in real-time and map your finger movements into drawing actions on a digital canvas.

Whether you want to draw for fun or explore the fundamentals of gesture-based interfaces, this project is a great starting point.

---

## 🌟 Core Features

🔍 **Real-Time Hand Tracking**
Utilizes MediaPipe to track up to 21 landmarks on each hand in real time.

🖌️ **Gesture-Based Drawing**
Draw on screen using your **index finger** — just like a magic pen.

🎨 **Dynamic Tool Selection**
Switch between colors or erase using **index + middle fingers** to select from a toolbar.

🔧 **Adjustable Brush Thickness**
Raise only your **pinky** finger and move it sideways to increase or decrease the brush size.

💡 **Intuitive Overlay UI**
A visual toolbar appears on top of the screen, and gesture selection gives immediate visual feedback.

---

## 👋 How It Works (Under the Hood)

The app uses specific hand gestures by checking the state of fingers (up/down). Based on that, it triggers specific functionalities:

| Gesture Pattern (`fingerUps()` return) | Fingers Raised        | Action                 |
| -------------------------------------- | --------------------- | ---------------------- |
| `01000`                                | Index only            | Drawing mode           |
| `01100`                                | Index + Middle        | Tool selection mode    |
| `00001`                                | Pinky only            | Adjust brush thickness |
| Any other                              | Other / Resting state | No action              |

🧠 The hand is tracked using **MediaPipe’s Hands API**, which gives you 21 landmark points per hand (e.g., tip of index finger = point 8).

---

## 🖼 Folder Structure

```bash
HandControlledPainter/
├── Tools/                   # Toolbar icons (should be 1366x120 in size)
|   ├── 0.png                # Default toolbar
│   ├── 1.png                # Red color brush icon
│   ├── 2.png                # Green color brush icon
│   ├── 3.png                # Blue color brush icon
│   ├── 4.png                # Eraser icon
├── handTrackingModule.py        # Hand detection and gesture logic (using MediaPipe)
├── handControlledPainter.py     # Main application logic
```

> 📌 Make sure all toolbar images are 1366x120 pixels to align correctly with the top bar of the screen.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository (or Download ZIP)

```bash
git clone https://github.com/your-username/HandControlledPainter.git
cd HandControlledPainter
```

### 2. Install Required Packages

Ensure Python is installed, then install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Running the Application

```bash
python handControlledPainter.py
```

* The webcam will activate automatically.
* You'll see a canvas and the toolbar at the top.
* Use your gestures to interact.

🛑 **Press `q`** to exit the application.

---

## 🧪 Sample Workflow

Here's how a typical interaction works:

1. **Start the App** → Webcam feed appears, toolbar visible.
2. **Raise only your index finger** → Draw on the canvas.
3. **Raise index + middle finger** → Activate tool selection mode.

   * Hover over toolbar sections (Red, Green, Blue, Eraser) to switch tools.
4. **Raise only pinky finger** → Move hand left/right to increase/decrease brush thickness.
5. **Relax your hand** → Stops all actions.

---

## 💡 Customization Ideas

Want to make it your own? Here are some ideas:

* Add **undo/redo** functionality
* Add **shape drawing** (rectangle, circle)
* Create a **screenshot/save canvas** button
* Support **gesture-based clearing of canvas**
* Add **voice feedback** for tool changes

---

## 🤝 Credits

Built with 💙 by \[Your Name or Team Name]

* OpenCV for image processing
* MediaPipe by Google for landmark detection
* Python for the glue

---

## 📬 Contact / Contribution

Got suggestions or want to contribute?
Feel free to [open an issue](https://github.com/your-username/HandControlledPainter/issues) or submit a pull request!

---
