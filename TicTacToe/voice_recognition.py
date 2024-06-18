import cv2
import speech_recognition as sr
import asyncio
import websockets
import json


async def send_voice_recognition_data():
    uri = "ws://localhost:1313/VoiceRecognition"  # Ensure this matches the Unity WebSocket server address
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
                            'text': voice_text
                        }
                        await websocket.send(json.dumps(data))
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand the audio")
                        data = {
                            'text': ''
                        }
                        await websocket.send(json.dumps(data))
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                        data = {
                            'text': ''
                        }
                        await websocket.send(json.dumps(data))
            except sr.WaitTimeoutError:
                print("Listening timed out, retrying...")
            except Exception as e:
                print(f"Microphone error: {e}")

            await asyncio.sleep(0.1)

async def main():
    await send_voice_recognition_data()

if __name__ == "__main__":
    asyncio.run(main())
