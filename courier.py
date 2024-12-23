# Importing necessary libraries and modules
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
from bs4 import BeautifulSoup
import customtkinter as ctk
import pyspeedtest
import os
import getpath
import is_widget

# Declare global variable FRAME
FRAME = None

# Function to run yt courier algorithm
def run_courier(frame, textbox, url, output_path = "C:/Users/ASUS/Downloads", quality = "360p"):
    """
    This function contains an algorithm for downloading 
    videos from YouTube with a certain resolution
    (144p, 240p, 360p, 480p, 720p, 1080p)
    
    Default quality: 360p
    """

    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function

    # Function to displays the log in the log box (textbox)
    def log_message(message):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        textbox.configure(state = "normal")
        textbox.insert(ctk.END, message + "\n")
        textbox.configure(state = "disabled")
        textbox.yview(ctk.END)  # Automatically scroll to the end

    # Function to calculate estimated video and audio size
    def estimate_file_size(quality, duration):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        # Dictionary containing video bitrates in kbps for different video qualities
        video_bitrates = {
            "144p": 100,
            "240p": 200,
            "360p": 400,
            "480p": 500,
            "720p": 1000,
            "1080p": 1500
        }

        audio_bitrate = 128  # Bitrate for audio in kbps

        # Get the video bitrate based on the specified quality
        video_bitrate = video_bitrates.get(quality, 400)

        # Calculate video size in MB
        video_size = (video_bitrate * 1000 / 8) * duration / (1024 * 1024)

        # Calculate audio size in MB 
        audio_size = (audio_bitrate * 1000 / 8) * duration / (1024 * 1024)

        # Return the estimated sizes for video and audio
        return video_size, audio_size

    # Function to calculate internet speed
    def speed_test(error_log = getpath.base("bin/log/error_log.bin")):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        try:
            test = pyspeedtest.SpeedTest("www.google.com")  # Create a pyspeedtest object
            speed = test.download()  # Perform a download speed test

            # Return the results of the speed test
            return speed
        except pyspeedtest.ConnectionError as e:
            # If an error occurs, log the error
            with open(error_log, "wb") as file:
                text = f"An error occurred: {e}"

                file.write(text.encode("utf-8"))
                file.close()

            # Displays the log in the log box (textbox)
            log_message(f"[ERROR] A connection error occurred during the speed test")

            return 0.0
        except Exception as e:
            # If an error occurs, log the error
            with open(error_log, "wb") as file:
                text = f"An error occurred: {e}"

                file.write(text.encode("utf-8"))
                file.close()

            # Displays the log in the log box (textbox)
            log_message(f"[ERROR] An error occurred during the speed test")

            return 0.0

    # Function to get the title of the YouTube video from its URL
    def get_title(url, error_log = getpath.base("bin/log/error_log.bin")):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("meta", property = "og:title")["content"]

            return title
        except Exception as e:
            # If an error occurs, log the error
            with open(error_log, "wb") as file:
                text = f"An error occurred: {e}"

                file.write(text.encode("utf-8"))
                file.close()

            # Displays the log in the log box (textbox)
            log_message(f"[ERROR] Failed to get the video title [saved to: {error_log}]")

            return None

    # Function to get the size of a file
    def get_size(path):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        # Get the size of the file in bytes
        file_size_bytes = os.path.getsize(path)
        
        # Convert the size from bytes to megabytes
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        return file_size_mb

    # Function to create unique filename
    def create_unique(path, base_name = "Untitled_", ext = ".mp4", number = []):
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function

        # List all files in the directory
        files = os.listdir(path)

        # Filter out files that match the base name and extension
        for file in files:
            if file.startswith(base_name) and file.endswith(ext):
                # Extract the number from filenames like 'Untitled_1.mp4'
                number = [int(file.replace(f"{base_name}", "").replace(ext, ""))]

        # Generate the next file number
        if number != []:
            next_number = number[0] + 1
        else:
            next_number = 1

        return f"{base_name}{next_number}"  # Return the filename with the next number

    # Displays the log in the log box (textbox)
    log_message("[TASK 1] Initializing...")

    # Temp directory
    path = getpath.base("temp")

    # Get internet speed
    internet_speed = speed_test()

    # Error log path
    error_log = getpath.base("bin/log/error_log.bin")

    # Create the temporary directory if it does not exist
    if not os.path.exists(path): 
        os.makedirs(path)

    # Initialize the YouTube object with the URL and progress callback function
    youtube = YouTube(url, on_progress_callback = on_progress)

    # Get the duration of the video 
    duration = youtube.length

    # Get the video size and audio size in bytes
    video_size, audio_size = estimate_file_size(quality, duration)

    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully initialized [path: {path}, youtube: {url}, duration: {(duration / 60):.2f} min]")
    log_message(f"[TASK 2] Downloading video... [size (estimate): {video_size:.2f} MB, bandwidth: {((internet_speed / 1_000_000) / 8):.2f} MBps]")
    
    # Get the video stream with the specified quality and file extension
    video_stream = youtube.streams.filter(res = quality, file_extension = "mp4").first()

    # If a video stream is found, download it to the temporary directory
    if video_stream:
        video_stream.download(output_path = path, filename = "video.mp4")
    else:
        # If no video stream is found, log the error
        with open(error_log, "wb") as file:
            text = "Video stream not found"

            file.write(text.encode("utf-8"))
            file.close()

        # Displays the log in the log box (textbox)
        log_message(f"[ERROR] Failed to download the video [saved to: {error_log}]")

        return  # Stop the function execution

    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully downloaded the video [saved to: {path}/video.mp4]")
    log_message(f"[TASK 3] Downloading audio... [size (estimate): {audio_size:.2f} MB, bandwidth: {internet_speed / 1_000_000:.2f} Mbps]")

    # Get the audio stream with the specified file extension
    audio_stream = youtube.streams.filter(only_audio = True, file_extension = "mp4").first()

    # If an audio stream is found, download it to the temporary directory
    if audio_stream:
        audio_stream.download(output_path = path, filename = "audio.mp4")
    else:
        # If no audio stream is found, log the error
        with open(error_log, "wb") as file:
            text = "Audio stream not found"

            file.write(text.encode("utf-8"))
            file.close()

        # Displays the log in the log box (textbox)
        log_message(f"[ERROR] Failed to download the audio [saved to: {error_log}]")

        return  # Stop the function execution

    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully downloaded the audio [saved to: {path}/audio.mp4]")
    log_message(f"[TASK 4] Getting the video title... [url: {url}]")

    # Get the video title
    title = get_title(url) 

    if title == None:
        title = create_unique(output_path)  # Video title if title not found
    
    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully getting the video title [title: {title}]")
    log_message(f"[TASK 5] Combining video and audio... [video: {video_size:.2f} MB, audio: {audio_size:.2f}]")

    # Paths to the downloaded video and audio files
    video_path = f"{path}/video.mp4"
    audio_path = f"{path}/audio.mp4"
    
    # Construct the output file path with the title of the video
    output_name = f"{title}.mp4"
    output_path = f"{output_path}/{output_name}"

    try:
        # Load the video and audio clips using moviepy
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set the audio of the video to the downloaded audio
        output = video.set_audio(audio)
        
        # Write the final video file with the specified codecs
        output.write_videofile(output_path, codec = "libx264", audio_codec = "aac")

        video.close()  # Close the video clip
        audio.close()  # Close the audio clip
    except Exception as e:
        # If an error occurs, log the error
        with open(error_log, "wb") as file:
            text = f"An error occurred: {e}"

            file.write(text.encode("utf-8"))
            file.close()

        # Displays the log in the log box (textbox)
        log_message(f"[ERROR] Failed to combine video and audio [saved to: {error_log}]")

        return  # Stop the function execution 

    video_size = get_size(video_path)  # Get the size of the video file (temp)
    audio_size = get_size(audio_path)  # Get the size of the audio file (temp)

    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully combines video and audio [path: {output_path}]")
    log_message(f"[TASK 6] Delete temporary files... [video_path: {video_path}, size: {video_size:.2f} MB; audio_path: {audio_path}, size: {audio_size:.2f} MB]")

    # Deletes audio and video in temp directory if files exist
    for file_path in [video_path, audio_path]:
        if os.path.exists(file_path):
            os.remove(file_path)

    # Displays the log in the log box (textbox)
    log_message(f"[SUCCESS] Successfully deleted temporary files [free: {(video_size + audio_size):.2f} MB]")
    log_message(f"[FINAL] Output [path: {output_path}, size: {get_size(output_path):.2f}]")
    log_message(f"[END] Finished\n")
