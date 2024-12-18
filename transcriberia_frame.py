# Importing necessary libraries and modules
import transcriberia
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import audioproc
import os
import main
import popup
import threading
import cleaner
import requests

# List of supported video file extensions
VID_EXT = [".mp4", ".avi", ".mov"]

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Function to initialize the transcriber tool interface
def transcriber_tool(root, frame):
    """
    Initializes the transcriberia tool interface within the given root window.
    It performs the following steps:
    1. Cleans specific files by calling the clean_file function from the cleaner module.
    2. Destroys the existing frame.
    3. Creates a new custom tkinter frame with specified dimensions and color.
    4. Adds a label, entry widget for drag-and-drop, and language selection buttons.
    5. Sets up the result display area.
    
    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the transcriberia tool interface
    """

    global LAST_PRESSED

    # Resets variable values
    LAST_PRESSED = None

    # Clean specific files using the cleaner module
    cleaner.clean_file()

    # Destroy the existing frame
    frame.destroy()

    # Create a new frame with specified width, height, and background color
    frame = ctk.CTkFrame(root, width = 800, height = 640, fg_color = main.FRAME_COLOR)
    frame.grid(row = 0, column = 1, padx = (8, 16), pady = 16, sticky = "nsew")
    frame.grid_columnconfigure(0, weight = 1)

    # Add a label for the transcriber tool frame
    transcribe_label = ctk.CTkLabel(frame, text = "Transcriberia", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR, justify = "center")
    transcribe_label.grid(row = 0, column = 0, padx = 24, pady = (24, 16), sticky = "nsew")

    # Variable to store the path of the dropped video file
    entry_var = ctk.StringVar()
    entry_var.set("Drop Video Here")

    # Function to handle the drop event for the entry widget
    def on_drop(event): 
        path = event.data.strip("{}")
        extension = os.path.splitext(path)[1]
        name = os.path.basename(path)

        if extension not in VID_EXT:
            entry_var.set("Extension is not supported")
            entry.after(2000, lambda: entry_var.set("Drop Video Here"))
        else:
            with open("bin/log/path_log.bin", "wb") as file:
                file.write(path.encode("utf-8"))
                file.close()

            entry.configure(state = "normal")
            entry_var.set(name) 
            entry.configure(state = "disabled")

    # Entry widget for drag-and-drop video files
    entry = ctk.CTkEntry(frame, textvariable = entry_var, height = 120, justify = "center", width = 860, corner_radius = 8,
                         font = (main.FONT, 16, "bold"), text_color = main.FADED_TEXT_COLOR, border_color = main.BORDER_COLOR,
                         border_width = 2, fg_color = main.ENTRY_COLOR) 
    entry.grid(row = 1, column = 0, padx = 160, pady = (16, 4), sticky = "nsew")
    entry.configure(state = "disabled")

    entry.drop_target_register(DND_FILES) 
    entry.dnd_bind('<<Drop>>', on_drop)

    # Label to display supported video file extensions
    ext_label = ctk.CTkLabel(frame, text = f"Extension: {", ".join(VID_EXT)}", font = (main.FONT, 10, "normal"), text_color = main.FADED_LABEL_COLOR)
    ext_label.grid(row = 2, column = 0, padx = 12, pady = 0, sticky = "nsew")

    # Language selection frames and canvases
    lang_selection_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR) 
    lang_selection_frame.grid(row = 3, column = 0, padx = 160, pady = 4, sticky = "nsew") 
    lang_selection_frame.grid_columnconfigure(0, weight = 1)

    lang_selection_canvas = ctk.CTkCanvas(lang_selection_frame, height = 28) 
    lang_selection_canvas.grid(row = 0, column = 0, sticky = "nsew") 
    lang_selection_canvas.grid_columnconfigure(0, weight = 1)

    lang_button_frame = ctk.CTkFrame(lang_selection_canvas, height = 28, fg_color = main.FRAME_COLOR) 
    lang_button_frame.grid(row = 0, column = 0, sticky = "nsew") 

    frame.grid_columnconfigure(3, weight = 1)

    # Horizontal scrollbar 
    scrollbar = ctk.CTkScrollbar(lang_selection_frame, orientation = "horizontal", command = lang_selection_canvas.xview, height = 12,
                                 button_color = main.SCROLLBAR_COLOR, button_hover_color = main.SCROLLBAR_HOVER_COLOR) 
    scrollbar.grid(row = 1, column = 0, sticky = "nsew") 
    
    # Configure canvas for scrollbar 
    lang_selection_canvas.configure(xscrollcommand = scrollbar.set) 
    lang_selection_canvas.create_window((0, 0), window = lang_button_frame, anchor = "nw") 
    
    # Update scroll region when the frame size changes 
    lang_button_frame.bind("<Configure>", lambda e: lang_selection_canvas.configure(scrollregion = lang_selection_canvas.bbox("all")))

    # Function to handle language selection
    def lang(event, button):
        button_name = button.cget("text")

        with open("bin/log/lang_log.bin", "wb") as file:
            if button_name in main.LANG:
                bin_lang = main.LANG[button_name]

                file.write(bin_lang.encode("utf-8"))

            file.close()

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

    # Function to create a language selection button
    def lang_button(text, row, column, frame):
        button = ctk.CTkButton(frame, text = text, font = (main.FONT, 10, "bold"), border_color = main.BORDER_COLOR, 
                               text_color = main.FADED_TEXT_COLOR, fg_color = main.FRAME_COLOR, height = 24, width = 86,
                               border_width = 1, hover_color = main.ENTRY_COLOR, command = lambda: change_button_color(button))
        button.grid(row = 0, column = column, padx = 4, pady = 4, sticky = "nsew")
        button.bind("<Button-1>", lambda event: lang(event, button))

        return button

    # Language selection buttons
    lang_buttons = ["Afrikaans", "Arabic", "Chinese", "Dutch", "English (US)", "English (UK)", "French", 
                    "German", "Hindi", "Indonesian", "Italian", "Japanese", "Javanese", "Korean", "Malaysia", 
                    "Portuguese", "Russian", "Spanish", "Sundanese", "Thai", "Turkish", "Vietnamese" ] 
                    
    for index, lang_name in enumerate(lang_buttons): 
        lang_button(lang_name, 0, index, lang_button_frame)

    # Frame for displaying the transcription result
    result_frame = ctk.CTkFrame(frame, height = 120, fg_color = main.FRAME_COLOR, border_color = main.BORDER_COLOR, border_width = 2,
                                corner_radius = 8)
    result_frame.grid(row = 5, column = 0, padx = 160, pady = (32, 0), sticky = "nsew")

    # Label to display the transcription progress
    loading_label = ctk.CTkLabel(result_frame, text = "Transcribing (0.0%)", font = (main.FONT, 16, "bold"), text_color = main.FADED_LABEL_COLOR) 
    loading_label.grid(row = 0, column = 0, padx = int((result_frame.winfo_reqwidth() / 2)), pady = int((result_frame.winfo_reqheight() / 2) + 16), 
                    sticky = "nsew") 
    loading_label.grid_forget()  # Hide the label initially

    # Textbox to display the transcription result
    result_box = ctk.CTkTextbox(result_frame, height = 120, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
    result_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
    result_box.configure(state = "disabled")  # Disable editing the textbox
    result_box.grid()

    # Configure the grid layout for the result_frame
    result_frame.grid_columnconfigure(0, weight = 1)
    result_frame.grid_rowconfigure(0, weight = 1)

    # Function to transcribe audio from a video file
    def transcribe():
        """
        Transcribes audio from a video file and updates the transcription progress in a GUI.
        It reads the video path and language from log files, processes the audio, and displays the transcription.
        """

        # Read the video path from the log file
        with open("bin/log/path_log.bin", "rb") as file:
            path = file.read()
            path = path.decode("utf-8")

            file.close()

        # Read the language from the log file
        with open("bin/log/lang_log.bin", "rb") as file:
            lang = file.read()
            lang = lang.decode("utf-8")

            file.close()

        # Check if the path or language is empty
        if path == "" or lang == "":
            popup.open_popup("Please drop a video and choose a language", True)

            loading_label.grid_forget()
            result_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
        else:
            # Display loading label and hide the result box
            loading_label.grid(row = 0, column = 0, padx = int((result_frame.winfo_reqwidth() / 2)), pady = int((result_frame.winfo_reqheight() / 2)), 
                        sticky = "nsew")
            result_box.grid_forget()
            
            # Call the transcriber function to process the video
            transcriberia.transcriber(path, lang, loading_label, "Transcribing")
            
            # Read the transcription result from the output file
            with open("bin/out/out.bin", "rb") as file:
                result = file.read()
                result = result.decode("utf-8")

                if result == "":
                    # Display an error message if transcription failed
                    loading_label.grid_forget()
                    result_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")

                    popup.open_popup("Failed to transcribe,\ntry checking your internet connection\nor the video contains a lot of noise", True)
                else:
                    # Display the transcription result in the result box
                    result_box.configure(state = "normal")
                    result_box.insert("1.0", result)
                    result_box.configure(state = "disabled")

                    loading_label.grid_forget()
                    result_box.grid(row = 0 , column = 0, padx = 12, pady = 12, sticky = "nsew")

                file.close()

    # Function to start the transcription process in a separate thread
    def start_transcribe():
        """
        Starts the transcription process in a separate thread to avoid blocking the GUI.
        """

        def check_internet_connection(url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'transcribe' function.
            If the connection fails, it will show a popup message to check the internet connection.
            
            :param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'transcribe' function
                    thread = threading.Thread(target = transcribe)

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Call the function to check the internet connection
        check_internet_connection()

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

    # Configure the row weight for the grid layout
    frame.grid_rowconfigure(5, weight = 1)

    # Button to start the transcription process
    transcribe_button = ctk.CTkButton(frame, text = "Transcribe", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                      hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, command = start_transcribe)
    transcribe_button.grid(row = 4, column = 0, padx = 360, pady = (12, 0), sticky = "nsew")

    # Button to copy the transcription result to the clipboard
    copy_button = ctk.CTkButton(frame, text = "Copy", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, command = get_value)
    copy_button.grid(row = 6, column = 0, padx = 360, pady = (16, 24), sticky = "nsew")
