import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess
from collections import deque

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(0)

# Blink thresholds
EAR_THRESH = 0.21
BLINK_MIN = 0.25
BLINK_MAX = 0.7
LONG_BLINK = 2.0

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# Origin calibration
origin_left, origin_right = None, None
screen_w, screen_h = pyautogui.size()

# Blink tracking
blink_start = None
last_blink_time = 0
blink_count = 0

# Debounce
COOLDOWN = 1.0
last_action_time = 0

# Cursor smoothing
positions = deque(maxlen=7)

def euclidean(p1, p2, w, h):
    return ((p1.x * w - p2.x * w) ** 2 + (p1.y * h - p2.y * h) ** 2) ** 0.5

def eye_aspect_ratio(landmarks, eye, w, h):
    v1 = euclidean(landmarks[eye[1]], landmarks[eye[5]], w, h)
    v2 = euclidean(landmarks[eye[2]], landmarks[eye[4]], w, h)
    h_len = euclidean(landmarks[eye[0]], landmarks[eye[3]], w, h)
    return (v1 + v2) / (2.0 * h_len)

def get_eye_center(landmarks, ids, w, h):
    xs = [landmarks[i].x * w for i in ids]
    ys = [landmarks[i].y * h for i in ids]
    return int(sum(xs) / len(xs)), int(sum(ys) / len(ys))

def trigger_action(action):
    global last_action_time
    if time.time() - last_action_time > COOLDOWN:
        if action == "left_click":
            pyautogui.click()
        elif action == "double_click":
            pyautogui.doubleClick()
        elif action == "right_click":
            pyautogui.rightClick()
        elif action == "browser":
            subprocess.Popen("start chrome", shell=True)
        elif action == "notepad":
            subprocess.Popen("notepad.exe")
        elif action == "calc":
            subprocess.Popen("calc.exe")
        elif action == "explorer":
            subprocess.Popen("explorer")
        print("Action:", action)
        last_action_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Eye centers
        left_center = get_eye_center(landmarks, LEFT_IRIS, w, h)
        right_center = get_eye_center(landmarks, RIGHT_IRIS, w, h)

        # Draw iris
        cv2.circle(frame, left_center, 3, (0, 255, 0), -1)
        cv2.circle(frame, right_center, 3, (0, 255, 0), -1)

        # EAR (blink detection)
        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2

        if avg_ear < EAR_THRESH:  # Eyes closed
            if blink_start is None:
                blink_start = time.time()
        else:  # Eyes open
            if blink_start is not None:
                blink_time = time.time() - blink_start

                if BLINK_MIN <= blink_time <= BLINK_MAX:
                    if time.time() - last_blink_time < 0.5:
                        blink_count += 1
                    else:
                        blink_count = 1
                    last_blink_time = time.time()

                    if blink_count == 2:
                        trigger_action("double_click")
                        blink_count = 0
                    else:
                        trigger_action("left_click")

                elif blink_time >= LONG_BLINK:
                    print("Mode switch (long blink)")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

                blink_start = None

        # Right eye long blink = right click
        if right_ear < EAR_THRESH and avg_ear > EAR_THRESH:
            if blink_start is None:
                blink_start = time.time()
            elif time.time() - blink_start >= LONG_BLINK:
                trigger_action("right_click")
                blink_start = None

        if origin_left and origin_right:
            # Cursor movement
            dx = (left_center[0] - origin_left[0]) + (right_center[0] - origin_right[0])
            dy = ((left_center[1] + right_center[1]) // 2) - ((origin_left[1] + origin_right[1]) // 2)

            if abs(dx) < 10: dx = 0
            if abs(dy) < 8: dy = 0

            new_x = screen_w // 2 + dx * 10
            new_y = screen_h // 2 + dy * 10

            positions.append((new_x, new_y))
            avg_x = int(sum(p[0] for p in positions) / len(positions))
            avg_y = int(sum(p[1] for p in positions) / len(positions))

            pyautogui.moveTo(avg_x, avg_y, duration=0.1)

            # App shortcuts (require look + blink)
            if dy < -30 and avg_ear < EAR_THRESH:  # Look Up + Blink
                trigger_action("browser")
            elif dx < -40 and avg_ear < EAR_THRESH:  # Look Left + Blink
                trigger_action("notepad")
            elif dx > 40 and avg_ear < EAR_THRESH:  # Look Right + Blink
                trigger_action("calc")
            elif dy > 30 and avg_ear < EAR_THRESH:  # Look Down + Blink
                trigger_action("explorer")

        else:
            cv2.putText(frame, "Press 'o' to set origin", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("I.R.I.S. – Eye Mode (Stable)", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key to exit
        break
    elif key == ord('o') and results.multi_face_landmarks:
        origin_left = get_eye_center(landmarks, LEFT_IRIS, w, h)
        origin_right = get_eye_center(landmarks, RIGHT_IRIS, w, h)
        print("Origin set!")
    elif key == ord('q'):  # 'Q' key to exit
        print("Exiting program...")
        break

cap.release()
cv2.destroyAllWindows()
