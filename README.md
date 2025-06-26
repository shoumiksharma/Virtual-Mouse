# Virtual Mouse with MediaPipe and OpenCV

Control your computer mouse using hand gestures and a webcam!\
Move the cursor with your **index finger**, and **click** by touching your **thumb to pinky** — all with just one hand.

---

## 🖱️ Features

- ✅ One-hand control: no second hand needed for clicks.
- 🎯 Calibrate screen corners by pointing and confirming with a gesture.
- ⚡ Smooth, real-time control.
- 🖲️ Cursor movement with index finger.
- 👆 Mouse click by touching thumb and pinky of the same hand.

---

## 👷 Requirements

Install Python 3.7 or above and the following libraries:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## 🚀 How to Run

1. **Save the script** as `virtual_mouse.py`.

2. Open a terminal or command prompt in the folder containing the script.

3. Run the script:

```bash
python virtual_mouse.py
```

4. **Calibration**:

   - Point your **index finger** to each corner of the screen **(TOP-LEFT → TOP-RIGHT → BOTTOM-LEFT → BOTTOM-RIGHT)**.
   - For each corner, confirm by **touching your thumb and pinky together**.
   - Once all 4 corners are registered, calibration completes.

5. **Mouse Control**:

   - Move your **index finger** to control the mouse pointer.
   - Touch your **thumb and pinky** together to simulate a **mouse click**.

6. Press `Esc` key to **exit** the program.

---

## 📌 Tips

- Make sure you have **good lighting** for accurate hand detection.
- **Avoid background clutter** for best tracking performance.
- During calibration, ensure your hand is fully visible in the camera frame.

