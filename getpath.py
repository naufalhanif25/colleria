# Importing necessary libraries
import sys
import os

# Function to generate the base path for a given file or directory path
def base(path):
    try:
        # Try to get the base path 
        base = sys._MEIPASS
    except Exception as e:
        # Use the absolute path of the current directory
        base = os.path.abspath(".")

    # Join the base path with the provided relative path
    base = os.path.join(base, path)
    # Replace backslashes with forward slashes for consistency
    base = base.replace("\\", "/")

    return base # Return path
