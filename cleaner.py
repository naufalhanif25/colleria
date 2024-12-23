# Importing necessary libraries
import os
import getpath

# Function to cleans specified files
def clean_file():
    """
    This function cleans specified files by overwriting them with an empty content.
    The files include:
    - bin/out/out.bin
    - bin/log/path_log.bin
    - bin/log/lang_log.bin
    - bin/log/ext_log.bin
    - bin/log/q_log.bin
    """

    transcriber_file = ["bin/out/out.bin", "bin/log/path_log.bin", "bin/log/lang_log.bin",
                        "bin/log/ext_log.bin", "bin/log/q_log.bin"]
    
    for path in transcriber_file:
        path = getpath.base(path)  # Get the absolute path of the file

        # Open the file in write mode to overwrite its content with empty content
        with open(path, "wb") as file:
            pass
        
        # Close the file after cleaning (not strictly necessary as the 'with' statement handles it)
        file.close()

    # Deletes audio and video in temp directory if files exist
    for file_path in ["temp/video.mp4", "temp/audio.mp4"]:
        file_path = getpath.base(file_path)  # Get the absolute path of the file

        if os.path.exists(file_path):
            os.remove(file_path)

def clean_audio(directory="temp"):
    """
    Function to clean audio files from a specified directory,
    except for the .gitkeep file.

    Parameters:
    - directory: The directory to clean audio files from (default is "temp").

    """

    path = getpath.base(directory)  # Get the absolute path of the specified directory
    files = os.listdir(path)  # Get a list of all files in the directory

    # Iterate through each file in the directory
    for file in files:
        # Get the absolute path of the current file
        file_path = getpath.base(f"{directory}/{file}")

        # Check if the current item is a file and not .gitkeep
        if os.path.isfile(file_path) and file != ".gitkeep":
            os.remove(file_path)  # Remove the file
