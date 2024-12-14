# Importing necessary libraries and modules
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.signal import butter, lfilter
import speech_recognition as sr
import transcriberia
import os

# Variable initialization
DIR = "temp"
BITRATE = "8k"

"""
This code contains functions for processing audio 
that has been extracted from the finished video. 
The processing carried out includes splitting the audio 
into several parts and denoising.
"""

# Function to split audio into parts
def super_trim():
    """
    Splits the audio file into chunks based on silence and exports the chunks as separate wav files.
    """

    SILENCE_THRESH = -50 # Threshold for silence detection in dB
    MIN_SILENCE = 200 # Minimum silence duration in ms
    KEEP_SILENCE = 1000 # Keep silence for this duration in ms
    MAX_DURATION = 10000 # Maximum duration of a segment in ms
    
    # Check if the directory exists and remove any files if it does
    if os.path.exists(DIR):
        listdir = os.listdir(DIR)

        for file in listdir:
            file_path = os.path.join(DIR, file)

            if os.path.isfile(file_path):
                os.remove(file_path)

    # Load the audio file
    audio = AudioSegment.from_file(transcriberia.OUT)
        
    # Check if the output file exists and create the directory if it doesn't
    if os.path.exists(transcriberia.OUT):
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        
        # Split the audio into chunks based on silence
        chunks = split_on_silence(audio, 
                                  min_silence_len = MIN_SILENCE, 
                                  silence_thresh = SILENCE_THRESH, 
                                  keep_silence = KEEP_SILENCE)
        
        audio_chunk = []
        
        # Split the chunks further if they are longer than the maximum duration
        for chunk in chunks:
            audio_chunk.extend([chunk[i:i + MAX_DURATION] for i in range(0, len(chunk), MAX_DURATION)])
        
        # Export each chunk as a separate wav file
        for index, chunk in enumerate(audio_chunk):
            chunk_path = os.path.join(DIR, f"chunk_{index}.wav")
            chunk.export(chunk_path, format = "wav", bitrate = BITRATE)

# Function to return the filter coefficients
def butter_bandpass(lowcut, highcut, fs, order = 5):
    nyq = 0.5 * fs # Nyquist frequency
    low = lowcut / nyq # Normalized low cutoff frequency
    high = highcut / nyq # Normalized high cutoff frequency
    b, a = butter(order, [low, high], btype = "band") # Get the filter coefficients

    return b, a

# Function to apply the filter to the audio
def bandpass_filter(data, lowcut, highcut, fs, order = 5):
    b, a = butter_bandpass(lowcut, highcut, fs, order = order) # Get the filter coefficients
    y = lfilter(b, a, data) # Apply the filter

    return y

# Function to denoiser the audio
def audio_denoiser(input_path):
    LOWCUT = 300 # Low cutoff frequency for the bandpass filter in Hz
    HIGHCUT = 3000 # High cutoff frequency for the bandpass filter in Hz

    # Load the audio file
    audio_segment = AudioSegment.from_wav(input_path)

    # Get the audio samples as a numpy array
    samples = np.array(audio_segment.get_array_of_samples()) 

    # Sampling rate of the audio in Hz
    fs = audio_segment.frame_rate 

    # Apply the bandpass filter
    filtered_samples = bandpass_filter(samples, LOWCUT, HIGHCUT, fs) 

    # Create a new audio segment with the filtered samples
    filtered_segment = audio_segment._spawn(filtered_samples.astype(np.int16).tobytes())

    # Export the filtered audio as a wav file
    filtered_segment.export(transcriberia.OUT, format = "wav", bitrate = BITRATE) 
