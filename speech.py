import os
from playsound import playsound
import requests
import gtts
from dotenv import load_dotenv

load_dotenv()


# TODO: Nicer names for these ids
voices = ["ErXwobaYiN019PkySvjV", "EXAVITQu4vr4xnSDxMaL", "MF3mGyEYCl7XYWbV9V6O"]

tts_headers = {
    "Content-Type": "application/json",
    "xi-api-key": os.getenv("ELEVENLABS_APIKEY")
}

def eleven_labs_speech(text, voice_index):
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
        voice_id=voices[voice_index])
    formatted_message = {"text": text}
    response = requests.post(
        tts_url, headers=tts_headers, json=formatted_message)

    print(response.status_code)
    if response.status_code == 200:
        with open("speech.mpeg", "wb") as f:
            f.write(response.content)
        playsound("speech.mpeg")
        os.remove("speech.mpeg")
        return True
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
        os.remove("speech.mpeg")
        return False

def gtts_speech(text):
    tts = gtts.gTTS(text)
    tts.save("speech.mp3")
    playsound("speech.mp3")
    os.remove("speech.mp3")

def say_text(text, voice_index=2):
    if not os.getenv("ELEVENLABS_APIKEY"):
        gtts_speech(text)
    else:
        success = eleven_labs_speech(text, voice_index)
        if not success:
            gtts_speech(text)
