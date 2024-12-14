# Importing necessary libraries and modules
import moviepy.editor as mp
import speech_recognition as sr
import audioproc
import os

# Variable initialization
RAW = "audio/raw.wav"
OUT = "audio/out.wav"

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

    listdir = os.listdir(audioproc.DIR)
    scale = len(listdir) / 100
    percentage = inverse_percentage(len(listdir), count, scale)

    if count > 1 and percentage == 100.0:
        return

    label.configure(text = f"{text} ({percentage:.1f}%)")
    label.after(1000, percentage_label, label, text, count + 1)

# Function to transcribe audio from a video file
def transcriber(video_path, lang, label, label_text):
    """
    Transcribes audio from a video file and updates the transcription progress in a GUI.
    
    Parameters:
    - video_path: Path to the video file to be transcribed
    - lang: Language code for transcription
    - label: The label widget to display progress
    - label_text: The text to display along with the progress percentage
    """

    transcribe = []

    # Extract audio from the video file and save as raw.wav
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(RAW)

    recognizer = sr.Recognizer()
    sr.AudioFile(RAW)
    audioproc.audio_denoiser(RAW)
    os.remove(RAW)
    audioproc.super_trim()
    os.remove(OUT)

    # Count the number of audio chunks
    listdir = os.listdir(audioproc.DIR)
    sum_file = sum(1 for file in listdir if os.path.isfile(os.path.join(audioproc.DIR, file)))

    # Create or clean the output binary file
    with open("bin/out/out.bin", "wb") as file:
        pass

    # Transcribe each audio chunk
    for index in range(sum_file):
        audio = sr.AudioFile(os.path.join(audioproc.DIR, f"chunk_{index}.wav"))

        with audio as source:
            audio_data = recognizer.record(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data, language = lang)

            with open("bin/out/out.bin", "ab") as file:
                text = text + " "
                bin_text = text.encode("utf-8")

                file.write(bin_text)
                file.close()

        except sr.UnknownValueError:
            with open("bin/log/error_log.bin", "wb") as file:
                text = "Audio not recognized"

                file.write(text.encode("utf-8"))
                file.close()
        except sr.RequestError as e:
            with open("bin/log/error_log.bin", "wb") as file:
                text = f"Requests to the Google Speech Recognition service failed; {e}"
                
                file.write(text.encode("utf-8"))
                file.close()

        # Update the percentage label in the GUI
        percentage_label(label, label_text, 0) 
        
        # Remove the processed audio chunk
        os.remove(os.path.join(audioproc.DIR, f"chunk_{index}.wav"))
