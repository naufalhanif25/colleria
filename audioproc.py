# Importing necessary libraries and modules
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.signal import butter, lfilter
from scipy.io import wavfile
import noisereduce as nr
import speech_recognition as sr
import transcriberia
import os
import getpath
import is_widget

# Variable initialization
DIR = getpath.base("temp")
BITRATE = "8k"

# Declare global variable FRAME
FRAME = None

"""
This code contains functions for processing audio 
that has been extracted from the finished video. 
The processing carried out includes splitting the audio 
into several parts and denoising.
"""

# Function to split audio into parts
def super_trim(frame):
    """
    Splits the audio file into chunks based on silence and exports the chunks as separate wav files.
    """

    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function

    SILENCE_THRESH = -50 # Threshold for silence detection in dB
    MIN_SILENCE = 200 # Minimum silence duration in ms
    KEEP_SILENCE = 1000 # Keep silence for this duration in ms
    MAX_DURATION = 10000 # Maximum duration of a segment in ms
    
    # Check if the directory exists and remove any files if it does
    if os.path.exists(DIR):
        listdir = os.listdir(DIR)

        for file in listdir:
            file_path = os.path.join(DIR, file)

            # Skip .gitkeep file
            if file == ".gitkeep":
                continue

            # Remove other files
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
            loader_chunk = chunk + 12  # Increases audio volume by 12 dB
            
            loader_chunk.export(chunk_path, format = "wav", bitrate = BITRATE)

# Function to return the filter coefficients
def butter_bandpass(lowcut, highcut, fs, order = 5):
    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function
    
    nyq = 0.5 * fs # Nyquist frequency
    low = lowcut / nyq # Normalized low cutoff frequency
    high = highcut / nyq # Normalized high cutoff frequency
    b, a = butter(order, [low, high], btype = "band") # Get the filter coefficients

    return b, a

# Function to apply the filter to the audio
def bandpass_filter(data, lowcut, highcut, fs, order = 5):
    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function

    b, a = butter_bandpass(lowcut, highcut, fs, order = order) # Get the filter coefficients
    y = lfilter(b, a, data) # Apply the filter

    return y

# Function to reduce noise in audio file
def reduce_noise(input_path, output_path, chunk_size = 100000):
    """ 
    Reduces noise in an audio file by processing it in chunks. 
    Parameters: 
    - input_path: str, path to the input audio file. 
    - output_path: str, path to save the noise-reduced audio file. 
    - chunk_size: int, size of each chunk to process (default is 100000). 
    
    The function reads the audio file, splits it into smaller chunks, 
    reduces the noise in each chunk, and then concatenates and saves the result. 
    """
    
    # Read the audio file
    rate, data = wavfile.read(input_path)

    # If the audio has more than one channel (stereo), take the first channel
    if len(data.shape) > 1:
        data = data[:, 0]
    
    reduced_data = []
    
    # Process the audio in chunks
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        reduced_chunk = nr.reduce_noise(y = chunk, sr = rate)
        
        reduced_data.append(reduced_chunk)
    
    # Concatenate the processed chunks
    reduced_data = np.concatenate(reduced_data, axis = 0)
    
    # Save the noise-reduced audio to the specified output path
    wavfile.write(output_path, rate, reduced_data)

# Function to denoiser the audio
def audio_denoiser(frame, input_path):
    """ 
    Applies noise reduction and bandpass filter to the input audio file. 
    Parameters: 
    - frame: The frame of the application to check if it is destroyed. 
    - input_path: str, path to the input audio file. 
    
    The function performs noise reduction, applies a bandpass filter, 
    and saves the filtered audio to the specified output path. 
    """
    
    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function

    LOWCUT = 120 # Low cutoff frequency for the bandpass filter in Hz
    HIGHCUT = 8000 # High cutoff frequency for the bandpass filter in Hz
    
    # Perform noise reduction on the input audio file
    reduce_noise(input_path, transcriberia.OUT)

    # Load the audio file
    audio_segment = AudioSegment.from_wav(transcriberia.OUT)

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
