import pyttsx3
import speech_recognition as sr
import datetime
import os
# from clint.textui import progress
from bs4 import BeautifulSoup
from urllib.request import urlopen
from dotenv import load_dotenv
import openai
from speech import say_text;
# Import the required library

# Load variables from .env file
load_dotenv()

# Set up the OpenAI API credentials
openai.api_key = os.getenv('OPENAI_APIKEY')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

messages = [
    {"role": "system", "content": f"You are a helpful voice assistant, keep responses limited to 4 sentences. The current time is {datetime.datetime.now()}."},
]

def add_user_message(message):
    messages.append({
        "role": "user",
        "content": message
    })


def add_assistant_message(message):
    messages.append({
        "role": "assistant",
        "content": message
    })

# Define a function to generate text using the OpenAI API
def gen_response(prompt):
    add_user_message(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=256,
        messages=messages,
    )
    response_content = response['choices'][0]['message']['content']
    add_assistant_message(response_content)
    return response_content

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()
 
def takeCommand():
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
        response = gen_response(query)
        say_text(response)
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
     
    return ""
  
while True:
    takeCommand()
