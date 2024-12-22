# Importing necessary libraries and modules
import sounddevice
import soundfile
import threading

"""
This function is used to play sound effects
"""

# Function to play a sound from the given file path
def playsound(path):
    def play(path):
        # Read audio data and sampling rate from the file
        data, rate = soundfile.read(path, dtype = "float32")  
        
        # Play the audio data with the specified sampling rate
        sounddevice.play(data, rate)
        
        # Wait until the audio file has finished playing
        sounddevice.wait()

    # Create a new thread to play the sound
    thread = threading.Thread(target = play, args = (path,))

    thread.start()  # Start the thread
