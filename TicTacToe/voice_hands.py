import cv2
import mediapipe as mp
import asyncio
import websockets
import json
import speech_recognition as sr

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

async def send_hand_tracking_data(uri):
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
            print("HANDS")
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.1)

        cap.release()

async def send_voice_data(uri):
    async with websockets.connect(uri) as websocket:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            print("Ready to listen")

        while True:
            try:
                with mic as source:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=None)

                    try:
                        print("Recognizing...")
                        voice_text = recognizer.recognize_google(audio)
                        print(f"Recognized Text: {voice_text}")
                        data = {
                            'type': 'voice_recognition',
                            'text': voice_text
                        }
                        await websocket.send(json.dumps(data))
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand the audio")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                print("Listening timed out, retrying...")
            except Exception as e:
                print(f"Microphone error: {e}")

            await asyncio.sleep(0.1)

async def main():
    hand_tracking_uri = "ws://localhost:1313/HandTracking"
    voice_recognition_uri = "ws://localhost:1313/VoiceRecognition"

    # Create tasks for each coroutine
    task_hand_tracking = asyncio.create_task(send_hand_tracking_data(hand_tracking_uri))
    task_voice_recognition = asyncio.create_task(send_voice_data(voice_recognition_uri))

    # Gather and await both tasks
    await asyncio.gather(
        task_hand_tracking,
        task_voice_recognition
    )

if __name__ == "__main__":
    asyncio.run(main())
