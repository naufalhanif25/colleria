# Importing necessary libraries and modules
import customtkinter as ctk
import main
import cleaner

# Function to open the Notepedia frame
def notepedia_tool(root, frame):
   """
   This function initializes the notepedia tool interface 
   within the given root window. It performs the following steps: 
   1. Cleans specific files by calling the clean_file function from the cleaner module. 
   2. Destroys the existing tool_frame. 
   3. Creates a new custom tkinter frame with specified dimensions and color, 
      and places it within the root window. 

   Parameters:
   - root: The root window for the tkinter application
   - frame: The current tool_frame to be replaced with the notepedia tool interface
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
   frame.grid_rowconfigure(1, weight = 1)

   # Add a label for the notepedia tool frame
   notepedia_label = ctk.CTkLabel(frame, text = "Notepedia", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
   notepedia_label.grid(row = 0, column = 0, padx = 24, pady = (24, 12), sticky = "nsew")

   # Create a frame as a container
   container = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
   container.grid(row = 1, column = 0, padx = 12, pady = (0, 12), sticky = "nsew")
   container.grid_columnconfigure(0, weight = 1)
   container.grid_rowconfigure(1, weight = 1)

   header_frame = ctk.CTkFrame(container, height = 32, fg_color = main.FRAME_COLOR)
   header_frame.grid(row = 0, column = 0, padx = 8, pady = 8, sticky = "nsew")
   header_frame.grid_columnconfigure(0, weight = 1)
   header_frame.grid_rowconfigure(0, weight = 1)

   filename_frame = ctk.CTkFrame(header_frame, height = 32, fg_color = main.FRAME_COLOR)
   filename_frame.grid(row = 0, column = 0, padx = 0, pady = (8, 0), sticky = "w")

   filename_label = ctk.CTkLabel(filename_frame, text = "Untitled*", font = (main.FONT, 14, "normal"), text_color = main.TEXT_COLOR) 
   filename_label.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew") 
   filename_label.grid_forget()

   buttons_frame = ctk.CTkFrame(header_frame, width = 120, height = 32, fg_color = main.FRAME_COLOR)
   buttons_frame.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "e")

   buttons = ["New", "open", "Save"]

   for index, button_name in enumerate(buttons):
      if index == 0:
         padx = (8, 0)
      elif index == len(buttons) - 1:
         padx = 0
      else:
         padx = 8

      button = ctk.CTkButton(buttons_frame, text = button_name, font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                             hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, command = None)
      button.grid(row = 0, column = index, padx = padx, pady = 8, sticky = "nsew")

   log_box = ctk.CTkTextbox(container, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                            scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                            corner_radius = 8)
   log_box.grid(row = 1, column = 0, padx = 8, pady = (0, 8), sticky = "nsew")
