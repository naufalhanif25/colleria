# Importing necessary libraries
import os

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
        # Open the file in write mode to overwrite its content with empty content
        with open(path, "wb") as file:
            pass
        
        # Close the file after cleaning (not strictly necessary as the 'with' statement handles it)
        file.close()

    # Deletes audio and video in temp directory if files exist
    for file_path in ["temp/video.mp4", "temp/audio.mp4"]:
        if os.path.exists(file_path):
            os.remove(file_path)
