import cv2
import mediapipe as mp
import asyncio
import websockets
import json

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

async def send_hand_tracking_data():
    uri = "ws://localhost:1313/HandTracking"  # Ensure this matches the Unity WebSocket server address
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            right_hand_detected = False
            left_hand_detected = False
            right_hand_x, right_hand_y = 0, 0
            gesture = "none"

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    label = handedness.classification[0].label
                    if label == "Right":
                        right_hand_detected = True
                        x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                        right_hand_x = int(x * 1920)
                        right_hand_y = int(y * 1080)
                    elif label == "Left":
                        left_hand_detected = True
                        if (abs(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x -
                                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x) < 0.05 and
                            abs(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y -
                                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y) < 0.05):
                            gesture = "click"

            data = {
                'x': right_hand_x,
                'y': right_hand_y,
                'gesture': gesture,
                'right_hand_detected': right_hand_detected,
                'left_hand_detected': left_hand_detected
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.05)  # Slight delay to avoid overwhelming the server

        cap.release()

async def main():
    await send_hand_tracking_data()

if __name__ == "__main__":
    asyncio.run(main())
