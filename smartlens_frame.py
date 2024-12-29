# Importing necessary libraries and modules
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from PIL import Image 
from pytesseract import pytesseract 
from textblob import TextBlob
import threading
import queue
import requests
import os
import cleaner
import main
import getpath
import is_widget
import popup

# List of supported image extensions
EXT = [".png", ".jpg", ".jpeg"]

# Declare global variable FRAME
FRAME = None

# Variable to control loading animation state
ANIM = False

# Function to open the SmartLens frame
def smartlens_tool(root, frame):
    """
    This function initializes the samrtlens tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the smartlens tool interface
    """
    
    global ANIM
    
    # Resets variable values
    ANIM = False

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

    # Add a label for the smartlens tool frame
    smartlens_label = ctk.CTkLabel(frame, text = "SmartLens", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    smartlens_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")
    
    # Add a label for the ocr
    ocr_label = ctk.CTkLabel(frame, text = "with Tesseract OCR", font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR)
    ocr_label.grid(row = 1, column = 0, padx = 24, pady = (0, 12), sticky = "nsew")
    
    # Variable to store the path of the dropped image file
    entry_var = ctk.StringVar()
    entry_var.set("Drop Image Here")

    # Function to handle the drop event for the entry widget
    def on_drop(event): 
        path = event.data.strip("{}")
        extension = os.path.splitext(path)[1]
        name = os.path.basename(path).lower()

        if extension not in EXT:
            entry_var.set("Extension is not supported")
            entry.after(2000, lambda: entry_var.set("Drop Image Here"))
        else:
            with open(getpath.base("bin/log/path_log.bin"), "wb") as file:
                file.write(path.encode("utf-8"))

            entry.configure(state = "normal")
            entry_var.set(name) 
            entry.configure(state = "disabled")

    # Entry widget for drag-and-drop image files
    entry = ctk.CTkEntry(frame, textvariable = entry_var, height = 120, justify = "center", width = 860, corner_radius = 8,
                         font = (main.FONT, 16, "bold"), text_color = main.FADED_TEXT_COLOR, border_color = main.BORDER_COLOR,
                         border_width = 2, fg_color = main.ENTRY_COLOR) 
    entry.grid(row = 2, column = 0, padx = 160, pady = (16, 4), sticky = "nsew")
    entry.configure(state = "disabled")

    entry.drop_target_register(DND_FILES) 
    entry.dnd_bind('<<Drop>>', on_drop)
    
    # Label to display supported image file extensions
    ext_label = ctk.CTkLabel(frame, text = f"Extension: {", ".join(sorted(EXT))}", 
                             font = (main.FONT, 10, "normal"), text_color = main.FADED_LABEL_COLOR)
    ext_label.grid(row = 3, column = 0, padx = 12, pady = 0, sticky = "nsew")
    
    # Create a frame for the switch
    switch_frame = ctk.CTkFrame(frame, height = 12, fg_color = main.FRAME_COLOR)
    switch_frame.grid(row = 4, column = 0, padx = 160, pady = (2, 4), sticky = "nsew")
    switch_frame.grid_columnconfigure(0, weight = 1)
    
    # Create a switch
    switch_var = ctk.StringVar(value = 0)
    switch = ctk.CTkSwitch(switch_frame, variable = switch_var, text = "Autocorrect", font = (main.FONT, 10, "normal"), text_color = main.TEXT_COLOR, 
                           fg_color = main.SCROLLBAR_HOVER_COLOR, progress_color = main.FADED_BORDER_COLOR, button_color = main.FG_COLOR,
                           switch_height = 12, switch_width = 28, height = 12, width = 28, border_width = 0, button_hover_color = main.FG_HOVER_COLOR, 
                           offvalue = 0, onvalue = 1)
    switch.grid(row = 0, column = 0, padx = 12, pady = 0, sticky = "n")
    
    frame.grid_columnconfigure(0, weight = 1)
    
    # Frame for displaying the transcription result
    result_frame = ctk.CTkFrame(frame, height = 120, fg_color = main.FRAME_COLOR, border_color = main.BORDER_COLOR, border_width = 2,
                                corner_radius = 8)
    result_frame.grid(row = 6, column = 0, padx = 160, pady = (32, 0), sticky = "nsew")

    # Label to display the transcription progress
    loading_label = ctk.CTkLabel(result_frame, text = "Extracting", font = (main.FONT, 16, "bold"), text_color = main.FADED_LABEL_COLOR) 
    loading_label.grid(row = 0, column = 0, padx = 16, pady = 16, sticky = "nsew") 
    loading_label.grid_forget()  # Hide the label initially
    
    # Function to animate the loading label
    def animate_loading(label, text, delay = 400): 
        def update_text(): 
            if ANIM:
                current_text = label.cget("text") 

                if current_text.endswith("..."): 
                    label.configure(text = text) 
                else: 
                    label.configure(text = current_text + ".") 
                
                root.after(delay, update_text)  # Schedule the function to run again after the delay
    
        update_text()

    # Function to start the loading animation
    def start_animation(): 
        global ANIM
        
        ANIM = True 

        animate_loading(loading_label, "Extracting")

    # Function to stop the loading animation
    def stop_animation(): 
        global ANIM
        
        ANIM = False

    # Textbox to display the extraction result
    result_box = ctk.CTkTextbox(result_frame, height = 120, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
    result_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
    result_box.configure(state = "disabled")  # Disable editing the textbox
    result_box.grid()

    # Configure the grid layout for the result_frame
    result_frame.grid_columnconfigure(0, weight = 1)
    result_frame.grid_rowconfigure(0, weight = 1)
    
    frame.grid_rowconfigure(6, weight = 1)
    
    # Function to correct spelling mistakes in the input text
    def correct_text(queue_var, input_text):
        """
        Corrects spelling mistakes in the input text using TextBlob 
        and puts the corrected text in a queue.

        Parameters:
        - queue_var: queue.Queue, the queue to store the corrected text.
        - input_text: str, the text to be corrected.
        """
        
        blob = TextBlob(input_text)
        corrected_text = blob.correct()
    
        queue_var.put(str(corrected_text))  # Put corrected text
    
    # Function to extract image into text
    def extract(frame):
        """
        Extracts text from an image, corrects the spelling mistakes, and displays it in the result box.

        Parameters:
        - frame: the frame object to check for destruction and handle animations.
        """
    
        global FRAME
        
        FRAME = frame  # Assign the frame to the global variable FRAME
        
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function
    
        ocr = "C:/Program Files/Tesseract-OCR/tesseract.exe"  # Tesseract OCR Path
        
        # Open and read the path from a binary file
        with open(getpath.base("bin/log/path_log.bin"), "rb") as file:
            path = file.read()
            path = path.decode("utf-8")
                        
        # Check if the entry variable indicates no image is provided
        if entry_var.get() == "Drop Image Here":
            popup.open_popup("Please drop an image", True)
        else:
            start_animation()  # Start loading animation
            
            loading_label.grid(row = 0, column = 0, padx = 16, pady = 16, sticky = "nsew") 
            result_box.grid_forget()
            
            # Open the image and perform OCR
            image = Image.open(path) 
            pytesseract.tesseract_cmd = ocr
            text = pytesseract.image_to_string(image) 
            
            if switch_var.get() == 1:  # If the switch is on, correct spelling mistakes
                # Create a queue and thread to correct the text
                queue_var = queue.Queue()
                thread = threading.Thread(target = correct_text, args = (queue_var, text,))
                
                thread.start()  # Start the thread
                thread.join()  # Wait for the thread to finish
                
                final = queue_var.get()  # Get the final text from the queue
            else:
                final = text  # If the switch is off, use the original text
            
            result_box.configure(state = "normal")  # Enable editing the textbox
            result_box.insert(tk.END, final)
            result_box.configure(state = "disabled")  # Disable editing the textbox
            
            loading_label.grid_forget()
            result_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
            
            stop_animation()  # Stop loading animation
    
    # Function to start the extraction process in a separate thread
    def run_smartlens(frame):
        """
        Starts the document extraction process in a separate thread to avoid blocking the GUI.
        """

        def check_internet_connection(frame, url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'extract' function.
            If the connection fails, it will show a popup message to check the internet connection.
            
            :param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'extract' function
                    thread = threading.Thread(target = extract, args = (frame,))

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Call the function to check the internet connection
        check_internet_connection(frame)
    
    # Function to get the value from the result box and copy it to the clipboard
    def get_value():
        """
        Gets the transcription result from the result box and copies it to the clipboard.
        If the result box is empty, it displays an error message.
        """

        value = result_box.get("1.0", "end-1c")

        if value == "":
            popup.open_popup("No transcription available", True)
        else:
            root.clipboard_clear()
            root.clipboard_append(value)

            popup.open_popup("Copied to clipboard", True)
    
    # Button to start extracting images into text
    extract_button = ctk.CTkButton(frame, text = "Extract", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                   hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, command = lambda: run_smartlens(frame))
    extract_button.grid(row = 5, column = 0, padx = 360, pady = (12, 0), sticky = "nsew")
    
    # Button to copy the result to the clipboard
    copy_button = ctk.CTkButton(frame, text = "Copy", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, command = get_value)
    copy_button.grid(row = 7, column = 0, padx = 360, pady = 24, sticky = "nsew")
