# Importing necessary libraries and modules
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import popup
import main
import cleaner
import os
import threading
import requests
import doclab
import itertools

# List of supported file extensions
IMG_EXT = [".png", ".jpg", ".jpeg"]
EXT_DICT = [
    {".docx" : ".pdf"},
    {".doc" : ".pdf"},
    {".pdf" : ".docx"},
    {".pdf" : ".doc"},
    {".xlsx" : ".csv"},
    {".xls" : ".csv"},
    {".csv" : ".xlsx"},
    {".csv" : ".xls"},
    {".pptx" : ".pdf"},
    {".ppt" : ".pdf"},
    {".pdf" : ".pptx"},
    {".pdf" : ".ppt"},
]

# Adding image extensions dynamically to the list
EXT_DICT.extend([{ext : ".pdf"} for ext in IMG_EXT])
EXT_DICT.extend([{".pdf" : ext} for ext in IMG_EXT])

# Adding image extensions dynamically to the list
for ext_left in IMG_EXT:
    for ext_right in IMG_EXT:
        if ext_left != ext_right and [{ext_left : ext_right}] not in EXT_DICT:
            EXT_DICT.extend([{ext_left : ext_right}])

# Collect keys and values into separate lists
DICT_KEYS, DICT_VALUES = zip(*[(f"{key}", f"{value}") for ext_dict in EXT_DICT for key, value in ext_dict.items()])

# Variable to record the selected file extension
FILE_EXT = None

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Variable to control loading animation state
ANIM = False

# Variable to set completed conversions
DONE = False

# Function to open the DocLab frame
def doclab_tool(root, frame):
    """
    Initializes the doclab tool interface within the given root window. 
    It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
        and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the doclab tool interface
    """

    global LAST_PRESSED, FILE_EXT, ANIM, DONE

    # Resets variable values
    LAST_PRESSED = None
    FILE_EXT = None
    ANIM = False
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

    # Add a label for the doclab tool frame
    doclab_label = ctk.CTkLabel(frame, text = "DocLab", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    doclab_label.grid(row = 0, column = 0, padx = 24, pady = (24, 16), sticky = "nsew")\
    
    # Variable to store the path of the dropped video file
    entry_var = ctk.StringVar()
    entry_var.set("Drop File Here")

    # Function to handle the drop event for the entry widget
    def on_drop(event): 
        path = event.data.strip("{}")
        extension = os.path.splitext(path)[1]
        name = os.path.basename(path)

        if extension not in list(set(DICT_KEYS)):
            entry_var.set("Extension is not supported")
            entry.after(2000, lambda: entry_var.set("Drop File Here"))
        else:
            with open("bin/log/path_log.bin", "wb") as file:
                file.write(path.encode("utf-8"))
                file.close()

            entry.configure(state = "normal")
            entry_var.set(name) 
            entry.configure(state = "disabled")

    # Entry widget for drag-and-drop video files
    entry = ctk.CTkEntry(frame, textvariable = entry_var, height = 160, justify = "center", width = 860, corner_radius = 8,
                            font = (main.FONT, 16, "bold"), text_color = main.FADED_TEXT_COLOR, border_color = main.BORDER_COLOR,
                            border_width = 2, fg_color = main.ENTRY_COLOR) 
    entry.grid(row = 1, column = 0, padx = 160, pady = (16, 4), sticky = "nsew")
    entry.configure(state = "disabled")

    entry.drop_target_register(DND_FILES) 
    entry.dnd_bind('<<Drop>>', on_drop)

    # Label to display supported video file extensions
    ext_label = ctk.CTkLabel(frame, text = f"Extension: {", ".join(sorted(list(set(itertools.chain(DICT_VALUES, DICT_KEYS)))))}", 
                             font = (main.FONT, 10, "normal"), text_color = main.FADED_LABEL_COLOR)
    ext_label.grid(row = 2, column = 0, padx = 12, pady = 0, sticky = "nsew")

    # Extension selection frames and canvases
    ext_selection_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR) 
    ext_selection_frame.grid(row = 3, column = 0, padx = 160, pady = 4, sticky = "nsew") 
    ext_selection_frame.grid_columnconfigure(0, weight = 1)

    ext_selection_canvas = ctk.CTkCanvas(ext_selection_frame, height = 28) 
    ext_selection_canvas.grid(row = 0, column = 0, sticky = "nsew") 
    ext_selection_canvas.grid_columnconfigure(0, weight = 1)

    ext_button_frame = ctk.CTkFrame(ext_selection_canvas, height = 28, fg_color = main.FRAME_COLOR) 
    ext_button_frame.grid(row = 0, column = 0, sticky = "nsew") 

    frame.grid_columnconfigure(3, weight = 1)

    # Horizontal scrollbar 
    scrollbar = ctk.CTkScrollbar(ext_selection_frame, orientation = "horizontal", command = ext_selection_canvas.xview, height = 12,
                                    button_color = main.SCROLLBAR_COLOR, button_hover_color = main.SCROLLBAR_HOVER_COLOR) 
    scrollbar.grid(row = 1, column = 0, sticky = "nsew") 
    
    # Configure canvas for scrollbar 
    ext_selection_canvas.configure(xscrollcommand = scrollbar.set) 
    ext_selection_canvas.create_window((0, 0), window = ext_button_frame, anchor = "nw") 
    
    # Update scroll region when the frame size changes 
    ext_button_frame.bind("<Configure>", lambda e: ext_selection_canvas.configure(scrollregion = ext_selection_canvas.bbox("all")))

    # Create a text variable for the search entry and set a placeholder text
    output_entry_var = tk.StringVar() 
    output_entry_var.set("Browse path")

    frame.grid_rowconfigure(5, weight = 1)

    # Create a frame for the log components
    log_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
    log_frame.grid(row = 5, column = 0, padx = 160, pady = (0, 24), sticky = "nsew")
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

    # Create a frame for the loading label
    loading_frame = ctk.CTkFrame(log_frame, fg_color = main.BASE_COLOR, border_width = 2, border_color = main.BORDER_COLOR, corner_radius = 8)
    loading_frame.grid(row = 1, column = 0, padx = 0, pady = 0, sticky = "nsew")
    loading_frame.grid_columnconfigure(0, weight = 1)
    loading_frame.grid_rowconfigure(0, weight = 1)

    # Label to display the transcription progress
    loading_label = ctk.CTkLabel(loading_frame, text = "Converting", font = (main.FONT, 16, "bold"), text_color = main.FADED_LABEL_COLOR) 
    loading_label.grid(row = 0, column = 0, padx = 12, pady = 24, sticky = "nsew") 
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

        animate_loading(loading_label, "Converting")

    # Function to stop the loading animation
    def stop_animation(): 
        global ANIM
        
        ANIM = False

    # Function to handle extension selection
    def ext(event, button):
        button_name = button.cget("text")

        with open("bin/log/ext_log.bin", "wb") as file:
            if button_name in sorted(list(set(DICT_VALUES))):
                file.write(button_name.encode("utf-8"))

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
    def ext_button(text, row, column, frame):
        button = ctk.CTkButton(frame, text = text, font = (main.FONT, 10, "bold"), border_color = main.BORDER_COLOR, 
                                text_color = main.FADED_TEXT_COLOR, fg_color = main.FRAME_COLOR, height = 24, width = 86,
                                border_width = 1, hover_color = main.ENTRY_COLOR, command = lambda: change_button_color(button))
        button.grid(row = 0, column = column, padx = 4, pady = 4, sticky = "nsew")
        button.bind("<Button-1>", lambda event: ext(event, button))

        return button
                    
    for index, extension in enumerate(sorted(list(set(itertools.chain(DICT_VALUES, DICT_KEYS))))): 
        ext_button(extension, 0, index, ext_button_frame)

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

    # Function to convert file into a specific format
    def convert():
        global FILE_EXT, DONE

        # Read the document path from the log file
        with open("bin/log/path_log.bin", "rb") as file:
            path = file.read()
            path = path.decode("utf-8")

            file.close()

        # Read the extension path from the log file
        with open("bin/log/ext_log.bin", "rb") as file:
            FILE_EXT = file.read()
            FILE_EXT = FILE_EXT.decode("utf-8")

            file.close()
        
        output_path = output_entry_var.get()

        if path == "" or extension == "" or (output_path == "" or output_path == "Browse path"):
            popup.open_popup("Please drop a file or choose an extension or\nbrowse to the path for the output file", True)
        else:
            loading_label.grid(row = 0, column = 0, padx = 12, pady = 24, sticky = "nsew") 

            temp_path = os.path.basename(path)
            input_name, input_ext = os.path.splitext(temp_path)

            # Define a function to run doclab and handle stopping the animation
            def run(input_name, input_ext):
                global DONE

                # Function to truncate a string to a certain length and insert a newline
                def truncate(text, length = 64):
                    if len(text) <= length:
                        return text

                    # Truncate the string at the specified length and add a newline character
                    return text[:length] + '\n' + text[length:]

                def reset_animation():
                    # Hide the loading animation label
                    loading_label.grid_forget()

                    # Configure the text of the loading animation label
                    loading_label.configure(font = (main.FONT, 16, "bold"), text = "Converting")

                if any(input_ext == DICT_KEYS[index] and FILE_EXT == DICT_VALUES[index] for index in range(len(EXT_DICT))):
                    # Start the loading animation
                    start_animation()

                    # Run doclab
                    doclab.doclab(path, output_path, input_ext, FILE_EXT)

                    # Stop the loading animation
                    stop_animation()

                    # Truncate the input name
                    input_name = truncate(input_name)
                    
                    # Reset the animation
                    loading_label.configure(font = (main.FONT, 14, "bold"), text = f"The {input_name}{FILE_EXT}\nhas been saved to the destination")
                    root.after(2000, reset_animation)

                    # File conversion has been completed
                    DONE = True
                else:
                    popup.open_popup("Destination extensions are not supported", True)

                    # Hide the loading animation
                    loading_label.grid_forget()

            # Start the doclab process in a separate thread
            thread = threading.Thread(target = run, args = (input_name, input_ext,))
            
            thread.start()

    # Function to start the transcription process in a separate thread
    def run_doclab():
        """
        Starts the document conversion process in a separate thread to avoid blocking the GUI.
        """

        def check_internet_connection(url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'convert' function.
            If the connection fails, it will show a popup message to check the internet connection.
            
            :param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'convert' function
                    thread = threading.Thread(target = convert)

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Call the function to check the internet connection
        check_internet_connection()

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
    output_path_frame.grid(row = 4, column = 0, padx = 160, pady = (0, 8), sticky = "nsew")
    output_path_frame.grid_columnconfigure(0, weight = 1)
    output_path_frame.grid_rowconfigure(0, weight = 1)

    # Entry to display the output file path
    output_path_entry = ctk.CTkEntry(output_path_frame, textvariable = output_entry_var, height = 24, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                                corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_TEXT_COLOR, border_width = 2)
    output_path_entry.grid(row = 0, column = 0, padx = 0, pady = 12, sticky = "nsew")
    output_path_entry.configure(state = "disabled")

    # Create the browse button for output file path 
    browse_button = ctk.CTkButton(output_path_frame, text = "Browse", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, command = browse_directory)
    browse_button.grid(row = 0, column = 1, padx = (8, 0), pady = 12, sticky = "nsew")

    # Button to start the transcription process
    convert_button = ctk.CTkButton(output_path_frame, text = "Convert", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                    hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, command = run_doclab)
    convert_button.grid(row = 0, column = 2, padx = (8, 0), pady = 12, sticky = "nsew")
