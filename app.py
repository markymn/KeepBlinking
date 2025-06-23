import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import os
import numpy as np
import mediapipe as mp
from blink_detection import is_blink
import time
import sys
if sys.platform == 'win32':
    import ctypes

class BlinkDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KeepBlinking")
        self.root.configure(bg="black")
        self.root.geometry("320x220")
        self.root.resizable(False, False)

        # Set the window icon to blink.png
        icon_path = os.path.join(os.path.dirname(__file__), "blink.png")
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(False, icon)
            except:
                pass

        self.label = tk.Label(root, text="Blink Detection", font=("Roboto", 20), fg="white", bg="black")
        self.label.pack(pady=20)

        self.explanation = tk.Label(
            root,
            text="You should be blinking 10 times a minute.\nOr in other words, once every 6 seconds.\nI'll remind you.",
            font=("Roboto", 10),
            fg="white",
            bg="black"
        )
        self.explanation.pack(pady=(0, 10))

        # Single Start/Stop Button
        self.toggle_button = tk.Button(root, text="▶", command=self.toggle_detection, bg="gray", fg="white", font=("Roboto", 22, "bold"), width=6)
        self.toggle_button.pack(pady=20)

        self.running = False
        self.cap = None

        # Blink detection setup
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
        self.last_blink_time = time.time()
        self.blink_state = False
        self.cooldown_seconds = 1

        # Animated blink bars
        self.blink_top_bar = None
        self.blink_bottom_bar = None
        self.blink_bar_animating = False

    def toggle_detection(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.toggle_button.config(text="⏸")
            self.update_video()
        else:
            self.running = False
            self.toggle_button.config(text="▶")
            if self.cap:
                self.cap.release()
                self.cap = None
            self.hide_blink_bars()

    def show_blink_bars(self):
        if self.blink_top_bar or self.blink_bottom_bar or self.blink_bar_animating:
            return  # Already shown or animating
        self.blink_bar_animating = True
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        bar_height = int(screen_h * 0.15)
        # Create top bar
        self.blink_top_bar = tk.Toplevel(self.root)
        self.blink_top_bar.overrideredirect(True)
        self.blink_top_bar.attributes("-topmost", True)
        self.blink_top_bar.configure(bg="black")
        # Create bottom bar
        self.blink_bottom_bar = tk.Toplevel(self.root)
        self.blink_bottom_bar.overrideredirect(True)
        self.blink_bottom_bar.attributes("-topmost", True)
        self.blink_bottom_bar.configure(bg="black")
        # Animate bars in
        def animate_bars(step=0):
            if not self.blink_bar_animating:
                return
            max_steps = bar_height
            if step <= max_steps:
                # Top bar slides down
                self.blink_top_bar.geometry(f"{screen_w}x{step}+0+0")
                # Bottom bar slides up
                self.blink_bottom_bar.geometry(f"{screen_w}x{step}+0+{screen_h - step}")
                self.root.after(8, lambda: animate_bars(step + 1))
            else:
                self.blink_top_bar.geometry(f"{screen_w}x{bar_height}+0+0")
                self.blink_bottom_bar.geometry(f"{screen_w}x{bar_height}+0+{screen_h - bar_height}")
                self.blink_bar_animating = False
        animate_bars(0)

    def hide_blink_bars(self):
        self.blink_bar_animating = False
        if self.blink_top_bar is not None:
            self.blink_top_bar.destroy()
            self.blink_top_bar = None
        if self.blink_bottom_bar is not None:
            self.blink_bottom_bar.destroy()
            self.blink_bottom_bar = None

    def update_video(self):
        if self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                # --- Blink detection only, no display ---
                results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        left_eye, right_eye = [], []
                        for idx in self.LEFT_EYE_IDX:
                            lm = face_landmarks.landmark[idx]
                            x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                            left_eye.append((x, y))
                        for idx in self.RIGHT_EYE_IDX:
                            lm = face_landmarks.landmark[idx]
                            x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                            right_eye.append((x, y))
                        # Blink detection
                        blink, avg_ear = is_blink(left_eye, right_eye)
                        current_time = time.time()
                        if blink and not self.blink_state and (current_time - self.last_blink_time) > self.cooldown_seconds:
                            print("Blink detected!")
                            self.last_blink_time = current_time
                            self.blink_state = True
                        elif not blink:
                            self.blink_state = False

                # Show/hide blink warning bars if needed
                if time.time() - self.last_blink_time > 6:
                    self.show_blink_bars()
                else:
                    self.hide_blink_bars()

            self.root.after(15, self.update_video)
        else:
            if self.cap:
                self.cap.release()
                self.cap = None
            self.hide_blink_bars()

def main():
    root = tk.Tk()
    app = BlinkDetectionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()