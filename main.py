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
from sound_queue import wait_for_sound_queue
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

# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
def gen_streamed_response(prompt):
    add_user_message(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=256,
        messages=messages,
        stream=True,
    )
    return response

def chunk_streamed_response(prompt):
    # Openai chunks by token. From those chunks we want to break the streamed
    # response by sentence. We can use '.' as our separator or separate by length.
    # That way we can immediatly kickoff elevenlabs tts for each sentence and have it
    # play as our message is being generated for faster response time
    #
    # We should yield in our iterator anytime a new sentence_chunk is created
    INITIAL_MIN_SENTENCE_CHUNK_LEN = 60 # in num of tokens
    SENTENCE_CHUNK_LEN_INCR = 200 # Increment the min length of each new chunk in order to not overwhelm the elevenlabs api. Ideally we could use something like exponential backoff calculations:
    # https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html#error-handling-retrying-after-an-error
    CURRENT_SENTENCE_CHUNK_LEN = INITIAL_MIN_SENTENCE_CHUNK_LEN

    response = gen_streamed_response(prompt)
    collected_chunks = []
    current_sentence = ''
    for chunk in response:
        collected_chunks.append(chunk)
        chunk_message = chunk['choices'][0]['delta']
        if "content" in chunk_message:

            current_sentence += chunk_message["content"]
            if (chunk_message["content"] == '.' or chunk_message["content"] == "!" or chunk_message["content"] == "?") and len(current_sentence) > CURRENT_SENTENCE_CHUNK_LEN:
                yield current_sentence
                current_sentence = ''
                CURRENT_SENTENCE_CHUNK_LEN += SENTENCE_CHUNK_LEN_INCR
    
    if current_sentence != '':
        yield current_sentence

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()
 
def takeCommand():
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
        print('Waiting for sound queue...')
        wait_for_sound_queue()
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
        
        for sentence in chunk_streamed_response(query):
            print(sentence)
            say_text(sentence)
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
     
    return ""
  
while True:
    takeCommand()