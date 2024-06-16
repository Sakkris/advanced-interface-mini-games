import cv2
import mediapipe as mp
import socket
import json
import time

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to connect to the server
def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 1313))
            print("Connected to server")
            return sock
        except ConnectionRefusedError:
            print("Connection refused, retrying...")
            time.sleep(1)

# Set up the socket connection
sock = connect_to_server()

def send_data(sock, data):
    try:
        sock.sendall(json.dumps(data).encode('utf-8'))
        print("Data sent:", data)
    except (ConnectionAbortedError, BrokenPipeError, OSError) as e:
        print(f"Connection error: {e}")
        print("Reconnecting to server...")
        sock.close()
        sock = connect_to_server()  # Reassign the new socket after reconnecting
        try:
            sock.sendall(json.dumps(data).encode('utf-8'))  # Retry sending data
            print("Data sent after reconnection:", data)
        except Exception as e:
            print(f"Failed to send data after reconnection: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    right_hand_detected = False
    left_hand_detected = False
    screen_x, screen_y = 0, 0
    gesture = "none"

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label
            if label == "Right":
                right_hand_detected = True

                # Get the coordinates of the right hand index finger tip
                x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                # Normalize coordinates to screen size
                screen_x = int(x * 1920)
                screen_y = int(y * 1080)
                
            elif label == "Left":
                left_hand_detected = True

                # Detect gestures for the left hand
                if (abs(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x -
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x) < 0.05 and
                    abs(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y -
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y) < 0.05):
                    gesture = "click"

            # Draw hand landmarks for visualization
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    data = {
        'x': screen_x, 
        'y': screen_y, 
        'gesture': gesture,
        'right_hand_detected': right_hand_detected,
        'left_hand_detected': left_hand_detected
    }
    send_data(sock, data)

    cv2.imshow('Hand Tracking', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
sock.close()