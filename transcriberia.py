# Importing necessary libraries and modules
import moviepy.editor as mp
import speech_recognition as sr
import audioproc
import os
import getpath
import cleaner
import is_widget

# Variable initialization
RAW = getpath.base("audio/raw.wav")
OUT = getpath.base("audio/out.wav")

# Declare global variable FRAME
FRAME = None

# Function to calculate an inverse percentage
def inverse_percentage(value, count, scale):
    """
    Calculates an inverse percentage based on the given value, count, and scale.
    
    Parameters:
    - value: The current value to be used in the calculation
    - count: The current count or iteration number
    - scale: The scaling factor for the percentage calculation
    
    Returns:
    - The calculated percentage, or 0.0 if conditions are not met.
    """

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        cleaner.clean_audio()  # Delete the audio files

        return  # If the frame is destroyed, exit the function

    listdir = os.listdir(audioproc.DIR)

    if count >= 0 and len(listdir) > 0:
        percentage = 100 / (1 + (scale * value))
        return percentage
    else:
        return 0.0

# Function to update the percentage label in a GUI
def percentage_label(label, text, count):
    """
    Updates a label with the current percentage based on processed audio chunks.
    
    Parameters:
    - label: The label widget to be updated
    - text: The text to display along with the percentage
    - count: The current count or iteration number
    """

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        cleaner.clean_audio()  # Delete the audio files

        return  # If the frame is destroyed, exit the function

    listdir = os.listdir(audioproc.DIR)
    scale = len(listdir) / 100
    percentage = inverse_percentage(len(listdir), count, scale)

    if count > 1 and percentage == 100.0:
        return

    label.configure(text = f"{text} ({percentage:.1f}%)")
    label.after(1000, percentage_label, label, text, count + 1)

# Function to transcribe audio from a video file
def transcriber(frame, video_path, lang, label, label_text):
    """
    Transcribes audio from a video file and updates the transcription progress in a GUI.
    
    Parameters:
    - video_path: Path to the video file to be transcribed
    - lang: Language code for transcription
    - label: The label widget to display progress
    - label_text: The text to display along with the progress percentage
    """

    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        cleaner.clean_audio()  # Delete the audio files
        
        return  # If the frame is destroyed, exit the function

    transcribe = []

    try:
        # Extract audio from the video file and save as raw.wav
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(RAW)

        recognizer = sr.Recognizer()
        sr.AudioFile(RAW)
        audioproc.audio_denoiser(frame, RAW)
        os.remove(RAW)
        audioproc.super_trim(frame)
        os.remove(OUT)
    except FileNotFoundError:
        return

    # Count the number of audio chunks
    listdir = os.listdir(audioproc.DIR)
    sum_file = sum(1 for file in listdir if os.path.isfile(os.path.join(audioproc.DIR, file)))

    # Get the absolute path of the file
    out_path = getpath.base("bin/out/out.bin")
    error_path = getpath.base("bin/log/error_log.bin")

    # Create or clean the output binary file
    with open(out_path, "wb") as file:
        pass

    # Transcribe each audio chunk
    for index in range(sum_file - 1):
        try:
            audio = sr.AudioFile(os.path.join(audioproc.DIR, f"chunk_{index}.wav"))

            with audio as source:
                audio_data = recognizer.record(source)

            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio_data, language = lang)

                with open(out_path, "ab") as file:
                    text = text + " "
                    bin_text = text.encode("utf-8")

                    file.write(bin_text)

            except sr.UnknownValueError:
                with open(error_path, "wb") as file:
                    text = "Audio not recognized"

                    file.write(text.encode("utf-8"))
            except sr.RequestError as e:
                with open(error_path, "wb") as file:
                    text = f"Requests to the Google Speech Recognition service failed; {e}"
                    
                    file.write(text.encode("utf-8"))

            # Update the percentage label in the GUI
            percentage_label(label, label_text, 0) 
            
            try:
                # Remove the processed audio chunk
                os.remove(os.path.join(audioproc.DIR, f"chunk_{index}.wav"))
            except FileNotFoundError:
                return
        except FileNotFoundError:
            return

