import cv2
import mediapipe as mp
import time
from blink_detection import is_blink

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# Chin and forehead landmark indices
CHIN_IDX = 152
FOREHEAD_IDX = 10

cap = cv2.VideoCapture(0)

blink_count = 0
blink_state = False
last_blink_time = 0
cooldown_seconds = 1

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = []
            right_eye = []

            for idx in LEFT_EYE_IDX:
                lm = face_landmarks.landmark[idx]
                x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                left_eye.append((x, y))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            for idx in RIGHT_EYE_IDX:
                lm = face_landmarks.landmark[idx]
                x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                right_eye.append((x, y))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Chin point
            chin_lm = face_landmarks.landmark[CHIN_IDX]
            chin_x, chin_y = int(chin_lm.x * frame.shape[1]), int(chin_lm.y * frame.shape[0])
            cv2.circle(frame, (chin_x, chin_y), 4, (0, 0, 255), -1)  # Red dot for chin

            # Forehead point
            forehead_lm = face_landmarks.landmark[FOREHEAD_IDX]
            forehead_x, forehead_y = int(forehead_lm.x * frame.shape[1]), int(forehead_lm.y * frame.shape[0])
            cv2.circle(frame, (forehead_x, forehead_y), 4, (255, 0, 0), -1)  # Blue dot for forehead

            blink, avg_ear = is_blink(left_eye, right_eye)
            print(f"EAR: {avg_ear:.3f}", end="\r")

            current_time = time.time()
            if blink and not blink_state and (current_time - last_blink_time) > cooldown_seconds:
                blink_count += 1
                last_blink_time = current_time
                print(f"\n👁️ Blink detected! Total: {blink_count}")
                blink_state = True
            elif not blink:
                blink_state = False

    cv2.imshow("Eye Keypoints + Chin & Forehead", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
