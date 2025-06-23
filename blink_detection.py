import math

def euclidean_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def eye_aspect_ratio(eye):
    # eye = [p1, p2, p3, p4, p5, p6]
    A = euclidean_distance(eye[1], eye[5])  # vertical 1
    B = euclidean_distance(eye[2], eye[4])  # vertical 2
    C = euclidean_distance(eye[0], eye[3])  # horizontal
    if C == 0:
        return 0
    return (A + B) / (2.0 * C)

def is_blink(left_eye, right_eye, threshold=0.26):
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    avg_ear = (left_ear + right_ear) / 2.0
    return avg_ear < threshold, avg_ear