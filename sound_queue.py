import queue
import threading
import playsound
import os
import keyboard

sound_queue = queue.Queue()


def play_sounds():
    while True:
        # Dequeue the next sound file from the queue
        sound_file = sound_queue.get()

        # Play the sound file
        playsound.playsound(sound_file)
        os.remove(sound_file)  # Delete sound file after playing it

        # Mark the dequeued item as complete
        sound_queue.task_done()


def add_to_sound_queue(sound_file):
    # Add the sound file to the queue
    sound_queue.put(sound_file)


def clear_sound_queue():
    # Clear the sound queue properly, cleaning up remaining audio files

    while sound_queue.qsize() > 0:
        sound_file = sound_queue.get()
        print(sound_file)
        os.remove(sound_file)
        sound_queue.task_done()


def wait_for_sound_queue(allow_keyboard_skip=False):
    if not allow_keyboard_skip:
        sound_queue.join()
    else:
        while sound_queue.qsize() > 0:
            if keyboard.is_pressed(" "):
                clear_sound_queue()
                # TODO: we still need a way to cut the audio that is playing out.
                # See https://stackoverflow.com/questions/57158779/how-to-stop-audio-with-playsound-module
                break


# Start the thread for playing sounds
sound_thread = threading.Thread(target=play_sounds, daemon=True)
sound_thread.start()
