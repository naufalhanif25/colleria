# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import requests
import threading
import os
import main
import cleaner
import popup
import courier
import getpath

# List of supported video quality
QUALITY = ["144p", "240p", "360p", "480p", "720p", "1080p"]

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Variable to set completed conversions
DONE = False

# Function to open the YT Courier frame
def yt_courier_tool(root, frame):
   """
   This function initializes the yt courier tool interface 
   within the given root window. It performs the following steps: 
   1. Cleans specific files by calling the clean_file function from the cleaner module. 
   2. Destroys the existing tool_frame. 
   3. Creates a new custom tkinter frame with specified dimensions and color, 
      and places it within the root window. 

   Parameters:
   - root: The root window for the tkinter application
   - frame: The current tool_frame to be replaced with the yt courier tool interface
   """

   global DONE

   # Resets variable values
   DONE = False

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

   # Add a label for the yt courier tool frame
   yt_courier_label = ctk.CTkLabel(frame, text = "YT Courier", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
   yt_courier_label.grid(row = 0, column = 0, padx = 24, pady = (24, 32), sticky = "nsew")

   # Create a frame for the url entry and button
   url_frame = ctk.CTkFrame(frame, width = 860, height = 32, fg_color = main.FRAME_COLOR)
   url_frame.grid(row = 1, column = 0, padx = 160, pady = 0, sticky = "nsew")
   url_frame.grid_columnconfigure(0, weight = 1)
   url_frame.grid_rowconfigure(0, weight = 1)

   # Create a text variable for the url entry and set a placeholder text
   url_var = tk.StringVar() 
   url_var.set("Enter the YouTube URL")

   # Create a frame for the log components
   log_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
   log_frame.grid(row = 4, column = 0, padx = 160, pady = (0, 32), sticky = "nsew")
   log_frame.grid_columnconfigure(0, weight = 1)
   log_frame.grid_rowconfigure(1, weight = 1)

   # Create a frame for the message log frame and direct frame
   log_header_frame = ctk.CTkFrame(log_frame, fg_color = main.FRAME_COLOR)
   log_header_frame.grid(row = 0, column = 0, padx = 0, pady = (0, 12), sticky = "nsew")
   log_header_frame.grid_columnconfigure(0, weight = 1)
   log_header_frame.grid_columnconfigure(0, weight = 1)
   log_header_frame.grid_rowconfigure(0, weight = 1)

   # Create a frame for the message log label
   message_log_frame = ctk.CTkFrame(log_header_frame, fg_color = main.FRAME_COLOR)
   message_log_frame.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
   message_log_frame.grid_rowconfigure(0, weight = 1)

   # Create message log label
   message_log_label = ctk.CTkLabel(message_log_frame, text = "Message Log", font = (main.FONT, 14, "normal"), text_color = main.FADED_LABEL_COLOR) 
   message_log_label.grid(row = 0, column = 0, padx = 0, pady = (8, 0), sticky = "nsew") 

   # Textbox to display the transcription result
   log_box = ctk.CTkTextbox(log_frame, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                            scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                            border_color = main.BORDER_COLOR, border_width = 2, corner_radius = 8)
   log_box.grid(row = 1, column = 0, padx = 0, pady = 0, sticky = "nsew")
   log_box.configure(state = "disabled")  # Disable editing the textbox

   frame.grid_rowconfigure(4, weight = 1)

   q_path = getpath.base("bin/log/q_log.bin")  # Get the absolute path of the file

   # Function to handle entry click (focus in)
   def on_entry_click(event): 
      if url_var.get() == "Enter the YouTube URL": 
         url_entry.configure(text_color = main.TEXT_COLOR)
         url_var.set("") 

   # Function to handle entry focus out
   def on_focus_out(event): 
      if url_var.get() == "": 
         url_entry.configure(text_color = main.FADED_LABEL_COLOR)
         url_var.set("Enter the YouTube URL")

   # Function to run the yt courier algorithm
   def yt_courier(event = None):
      global DONE

      # Get the URL and output path from the user input fields
      url = url_entry.get()
      output_path = output_path_entry.get()

      # Open the binary log file to read the quality setting
      with open(q_path, "rb") as file:
         quality = file.read()  # Read the quality setting from the file
         quality = quality.decode("utf-8")  # Decode the binary data to a UTF-8 string

         # Close the file (this is done automatically with the 'with' statement)
         file.close()

      # Check if the URL, output path, and quality are not empty
      if (url != "" and url != "Enter the YouTube URL") and (output_path != "" and output_path != "Browse path") and quality != "":
         # Run the courier function with the provided URL, output path, and quality
         courier.run_courier(log_box, url, output_path, quality)

         # The video download has been completed
         DONE = True
      else:
         # Open a popup to notify the user to provide the necessary inputs
         popup.open_popup("Please drop a video or select quality\nor browse output directory", True)

   # Function to start the transcription process in a separate thread
   def run_yt_courier():
      """
      Starts the document conversion process in a separate thread to avoid blocking the GUI.
      """

      def check_internet_connection(url = "http://www.google.com/"):
         """
         This function checks the internet connection by sending an HTTP request to the provided URL.
         If the connection is successful, it will start a thread to run the 'yt_courier' function.
         If the connection fails, it will show a popup message to check the internet connection.
         
         :param url: URL used to check the internet connection. Default is http://www.google.com/
         """

         try:
            response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

            if response.status_code == 200:
               # If the connection is successful, start a thread to run the 'convert' function
               thread = threading.Thread(target = yt_courier)

               thread.start()
            else:
               # If the connection fails (status code is not 200), show a popup message
               popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
         except requests.ConnectionError:
            # If a connection error occurs, show a popup message
            popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

      # Call the function to check the internet connection
      check_internet_connection()

   # Entry to display the url
   url_entry = ctk.CTkEntry(url_frame, textvariable = url_var, width = 860, height = 32, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                            corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_TEXT_COLOR, border_width = 2)
   url_entry.grid(row = 0, column = 0, padx = 0, pady = (0, 2), sticky = "nsew")
   url_entry.bind("<FocusIn>", on_entry_click) 
   url_entry.bind("<FocusOut>", on_focus_out)
   url_entry.bind("<Return>", run_yt_courier)

   # Extension selection frames and canvases
   quality_selection_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR) 
   quality_selection_frame.grid(row = 2, column = 0, padx = 160, pady = (24, 12), sticky = "nsew") 
   quality_selection_frame.grid_columnconfigure(0, weight = 1)

   quality_selection_canvas = ctk.CTkCanvas(quality_selection_frame, height = 28) 
   quality_selection_canvas.grid(row = 0, column = 0, sticky = "nsew") 
   quality_selection_canvas.grid_columnconfigure(0, weight = 1)

   quality_button_frame = ctk.CTkFrame(quality_selection_canvas, height = 28, fg_color = main.FRAME_COLOR) 
   quality_button_frame.grid(row = 0, column = 0, sticky = "nsew") 

   frame.grid_columnconfigure(2, weight = 1)

   # Horizontal scrollbar 
   scrollbar = ctk.CTkScrollbar(quality_selection_frame, orientation = "horizontal", command = quality_selection_canvas.xview, height = 12,
                                   button_color = main.SCROLLBAR_COLOR, button_hover_color = main.SCROLLBAR_HOVER_COLOR) 
   scrollbar.grid(row = 1, column = 0, sticky = "nsew") 
   
   # Configure canvas for scrollbar 
   quality_selection_canvas.configure(xscrollcommand = scrollbar.set) 
   quality_selection_canvas.create_window((0, 0), window = quality_button_frame, anchor = "nw") 
   
   # Update scroll region when the frame size changes 
   quality_button_frame.bind("<Configure>", lambda e: quality_selection_canvas.configure(scrollregion = quality_selection_canvas.bbox("all")))

   # Function to change the color of the pressed button
   def change_button_color(button):
      global LAST_PRESSED

      # If there is a previously pressed button, reset its color
      if LAST_PRESSED is not None:
           LAST_PRESSED.configure(fg_color = main.FRAME_COLOR, hover_color = main.ENTRY_COLOR, text_color = main.FADED_TEXT_COLOR, 
                                  border_width = 1, border_color = main.BORDER_COLOR)

      # Change the color of the currently pressed button
      button.configure(fg_color = main.FG_COLOR, hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR,
                       border_width = 0, border_color = main.FRAME_COLOR)
       
      # Update the last pressed button to the current button
      LAST_PRESSED = button

   # Function to handle extension selection
   def quality(event, button):
      button_name = button.cget("text")

      with open(q_path, "wb") as file:
         if button_name in QUALITY:
            file.write(button_name.encode("utf-8"))

         file.close()

   # Function to create a quality selection button
   def quality_button(text, row, column, frame):
      button = ctk.CTkButton(frame, text = text, font = (main.FONT, 10, "bold"), border_color = main.BORDER_COLOR, 
                             text_color = main.FADED_TEXT_COLOR, fg_color = main.FRAME_COLOR, height = 24, width = 86,
                             border_width = 1, hover_color = main.ENTRY_COLOR, command = lambda: change_button_color(button))
      button.grid(row = 0, column = column, padx = 4, pady = 4, sticky = "nsew")
      button.bind("<Button-1>", lambda event: quality(event, button))

      return button
                   
   for index, extension in enumerate(QUALITY): 
      quality_button(extension, 0, index, quality_button_frame)

   # Function to browse for a directory
   def browse_directory():
      directory_path = tk.filedialog.askdirectory(
         title = "Select a Directory"
      )
      if directory_path:
         output_path_entry.configure(state = "normal")

         output_path_entry.delete(0, tk.END) 
         output_path_entry.insert(0, directory_path)
         output_path_entry.configure(text_color = main.TEXT_COLOR)
            
         output_path_entry.configure(state = "disabled") 

   # Function to open the output directory
   def open_directory(): 
      # Get the output path
      path = output_entry_var.get()

      if path != "" and DONE == True:
         # Open the specified directory using the default file manager 
         os.startfile(path)
      else:
         # If the path is empty
         popup.open_popup("No files have been converted yet", True)

   # Create a frame for the direct button
   direct_frame = ctk.CTkFrame(log_header_frame, fg_color = main.FRAME_COLOR)
   direct_frame.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "e")
   direct_frame.grid_rowconfigure(0, weight = 1)

   # Button to direct the user to the output directory
   direct_button = ctk.CTkButton(direct_frame, text = "Direct", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                 hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, command = open_directory)
   direct_button.grid(row = 0, column = 0, padx = 0, pady = (8, 0), sticky = "nsew")

   # Create a frame for the output path entry and button
   output_path_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR)
   output_path_frame.grid(row = 3, column = 0, padx = 160, pady = (0, 12), sticky = "nsew")
   output_path_frame.grid_columnconfigure(0, weight = 1)
   output_path_frame.grid_rowconfigure(0, weight = 1)

   # Create a text variable for the search entry and set a placeholder text
   output_entry_var = tk.StringVar() 
   output_entry_var.set("Browse path")

   # Entry to display the output file path
   output_path_entry = ctk.CTkEntry(output_path_frame, textvariable = output_entry_var, height = 32, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                                    corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_TEXT_COLOR, border_width = 2)
   output_path_entry.grid(row = 0, column = 0, padx = 0, pady = 12, sticky = "nsew")
   output_path_entry.configure(state = "disabled")

   # Create the browse button for output file path 
   browse_button = ctk.CTkButton(output_path_frame, text = "Browse", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                 hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, command = browse_directory)
   browse_button.grid(row = 0, column = 1, padx = (8, 0), pady = 12, sticky = "nsew")

   # Create the start button
   start_button = ctk.CTkButton(output_path_frame, text = "Start", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, 
                                command = run_yt_courier)
   start_button.grid(row = 0, column = 2, padx = (8, 0), pady = 12, sticky = "nsew")
