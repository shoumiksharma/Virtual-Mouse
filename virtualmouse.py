import cv2
import mediapipe as mp
import pyautogui
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smoothening = 7
clicking = False

calibration_points = []
corners = ['TOP-LEFT', 'TOP-RIGHT', 'BOTTOM-LEFT', 'BOTTOM-RIGHT']

def get_tip(landmarks, tip_index, width, height):
    tip = landmarks.landmark[tip_index]
    return int(tip.x * width), int(tip.y * height)

def is_thumb_pinky_touch(landmarks, width, height, threshold=40):
    tx, ty = get_tip(landmarks, 4, width, height)   # Thumb tip
    pkx, pky = get_tip(landmarks, 20, width, height)  # Pinky tip
    distance = np.hypot(tx - pkx, ty - pky)
    return distance < threshold

print("Calibration: Point with index finger. Confirm each corner by touching thumb and pinky.")

calibrated = False
while not calibrated:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        x, y = get_tip(hand, 8, width, height)
        cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)

        if len(calibration_points) < 4:
            cv2.putText(frame, f"Point to {corners[len(calibration_points)]} corner & tap Thumb + Pinky",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        if is_thumb_pinky_touch(hand, width, height):
            calibration_points.append((x, y))
            print(f"Captured {corners[len(calibration_points) - 1]} at ({x}, {y})")
            cv2.putText(frame, "Captured!", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Calibration", frame)
            cv2.waitKey(1000)

    cv2.imshow("Calibration", frame)

    if len(calibration_points) == 4:
        calibrated = True
        print("Calibration complete!")

    if cv2.waitKey(1) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        exit()

min_x = min(p[0] for p in calibration_points)
max_x = max(p[0] for p in calibration_points)
min_y = min(p[1] for p in calibration_points)
max_y = max(p[1] for p in calibration_points)

cv2.destroyAllWindows()
print("Starting virtual mouse...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        x, y = get_tip(hand_landmarks, 8, width, height)

        screen_x = np.interp(x, (min_x, max_x), (0, screen_width))
        screen_y = np.interp(y, (min_y, max_y), (0, screen_height))

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        if is_thumb_pinky_touch(hand_landmarks, width, height):
            if not clicking:
                pyautogui.click()
                clicking = True
                cv2.circle(frame, (x, y), 15, (0, 255, 0), cv2.FILLED)
        else:
            clicking = False

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
