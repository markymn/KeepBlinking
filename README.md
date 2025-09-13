# KeepBlinking

**KeepBlinking** is a desktop application that reminds you to blink—helping you maintain healthy eyes while using technology.

## Why Blinking Matters

Studies show that when we use screens, we blink far less than normal. Not blinking enough can cause a range of eye problems, including:

- **Dry, irritated eyes:** Reduced blinking causes the tear film to evaporate more quickly, leading to dryness, burning, and itching.
- **Blurred or double vision:** Eye muscles can become fatigued from prolonged focusing, resulting in blurry or double vision.
- **Headaches:** Eye strain can trigger headaches, often in the forehead or temples.
- **Eye fatigue:** Eyes may feel tired, sore, or heavy.
- **Difficulty concentrating:** Eye discomfort can make it hard to focus on the screen.
- **Watery eyes:** As a reflex, eyes may water to try and compensate for dryness.
- **Red eyes:** Irritation can cause blood vessels in the eyes to dilate, leading to redness.

You should be blinking at least **15 times a minute**. This program will remind you to blink if it notices you haven't blinked in 4 seconds, helping guarantee you blink at least 15 times per minute.

## How It Works

- Uses your webcam to detect blinks in real time.
- If you haven't blinked in 6 seconds, you'll get a visual reminder.
- The app runs quietly in the background with a simple, modern interface.

## Technologies Used

- **Python** for the application logic.
- **OpenCV** for live camera footage.
- **Google's MediaPipe** for accurate blink detection.
- **Tkinter** for the graphical user interface.

## Getting Started

1. Make sure you have Python 3.7+ installed.
2. Install the required dependencies:
   ```
   pip install opencv-python mediapipe pillow
   ```
3. Run the application:
   ```
   python app.py
   ```

## Notes

- You'll need a webcam for blink detection.
- For best appearance, install the [Roboto font](https://fonts.google.com/specimen/Roboto) on your system.
