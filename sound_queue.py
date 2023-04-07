import queue
import threading
from playsound import playsound
import os

sound_queue = queue.Queue()

def play_sounds():
    while True:
        # Dequeue the next sound file from the queue
        sound_file = sound_queue.get()

        # Play the sound file
        playsound(sound_file)
        os.remove(sound_file) # Delete sound file after playing it

        # Mark the dequeued item as complete
        sound_queue.task_done()

def add_to_sound_queue(sound_file):
    # Add the sound file to the queue
    sound_queue.put(sound_file)

# Start the thread for playing sounds
sound_thread = threading.Thread(target=play_sounds, daemon=True)
sound_thread.start()
    

# Example usage
# play_sound('example_sound_1.mp3')
# play_sound('example_sound_2.mp3')
# play_sound('example_sound_3.mp3')
# print('This code will continue running while the sounds play in the background.')
