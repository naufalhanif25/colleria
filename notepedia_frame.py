# Importing necessary libraries and modules
import customtkinter as ctk
import main
import cleaner

"""
This function initializes the Notepedia tool interface 
within the given root window. It performs the following steps: 
1. Cleans specific files by calling the clean_file function from the cleaner module. 
2. Destroys the existing tool_frame. 
3. Creates a new custom tkinter frame with specified dimensions and color, 
   and places it within the root window. 
"""

# Function to open the Notepedia frame
def notepedia_tool(root, frame):
   """
   Parameters:
   - root: The root window for the tkinter application
   - frame: The current tool_frame to be replaced with the transcriber tool interface
   """

   # Clean specific files using the cleaner module
   cleaner.clean_file()

   # Destroy the existing frame
   frame.destroy()

   # Create a new frame with specified width, height, and background color
   frame = ctk.CTkFrame(root, width = 800, height = 640, fg_color = main.FRAME_COLOR)

   # Position the new frame within the root window grid
   frame.grid(row = 0, column = 1, padx = (8, 16), pady = 16, sticky = "nsew")
   
   # Configure the column of the new frame to expand with available space
   frame.grid_columnconfigure(0, weight = 1)

   # Add a label for the notepedia tool frame
   notepedia_label = ctk.CTkLabel(frame, text = "Notepedia", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
   notepedia_label.grid(row = 0, column = 0, padx = 24, pady = (24, 16), sticky = "nsew")
