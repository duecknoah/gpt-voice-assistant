import os
from sound_queue import add_to_sound_queue
import requests
import gtts
from dotenv import load_dotenv
import threading
import uuid

load_dotenv()


# TODO: Nicer names for these ids
voices = ["ErXwobaYiN019PkySvjV", "EXAVITQu4vr4xnSDxMaL", "MF3mGyEYCl7XYWbV9V6O"]
tts_headers = {
    "Content-Type": "application/json",
    "xi-api-key": os.getenv("ELEVENLABS_APIKEY")
}

def generate_sound_uuid():
    return f"speech_{uuid.uuid4().hex}.mpeg"


def eleven_labs_speech(text, voice_index):
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
        voice_id=voices[voice_index])
    formatted_message = {"text": text}
    response = requests.post(
        tts_url, headers=tts_headers, json=formatted_message)

    if response.status_code == 200:
        uuid_filename = generate_sound_uuid()
        with open(uuid_filename, "wb") as f:
            f.write(response.content)
        add_to_sound_queue(uuid_filename)
        return True
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
        return False

def gtts_speech(text):
    tts = gtts.gTTS(text)
    file_name = generate_sound_uuid()
    tts.save(file_name)
    add_to_sound_queue(file_name)

def say_text(text, voice_index=2):
    if not os.getenv("ELEVENLABS_APIKEY"):
        gtts_speech(text)
    else:
        success = eleven_labs_speech(text, voice_index)
        if not success:
            gtts_speech(text)
