# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound 
import threading
import requests
import os
import cleaner
import main
import getpath
import is_widget
import popup

# Global variables to store the language
DOMAIN = "Auto detect"
TARGET = "Afrikaans"

# Language options available for translation
LANG = {"Auto detect" : "auto",
        "Afrikaans" : "af", 
        "Arabic" : "ar", 
        "Chinese" : "zh-CN", 
        "Dutch" : "nl", 
        "English" : "en", 
        "Filipino" : "tl", 
        "French" : "fr", 
        "German" : "de", 
        "Hindi" : "hi", 
        "Indonesian" : "id", 
        "Italian" : "it", 
        "Japanese" : "ja", 
        "Javanese" : "jw", 
        "Korean" : "ko", 
        "Malay" : "ms", 
        "Portuguese" : "pt", 
        "Russian" : "ru", 
        "Spanish" : "es", 
        "Sundanese" : "su", 
        "Thai" : "th", 
        "Turkish" : "tr", 
        "Vietnamese" : "vi"}

# Declare global variable FRAME
FRAME = None

# Function to open the Collenguist frame
def collenguist_tool(root, frame):
    """
    This function initializes the collenguist tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the collenguist tool interface
    """

    global DONE, DOMAIN, TARGET

    # Resets variable values
    DONE = False
    DOMAIN = "Auto detect"
    TARGET = "Afrikaans"

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

    # Add a label for the collenguist tool frame
    collenguist_label = ctk.CTkLabel(frame, text = "Collenguist", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    collenguist_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")

    # Add a label for the llm
    llm_label = ctk.CTkLabel(frame, text = "with Google Translate", font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR)
    llm_label.grid(row = 1, column = 0, padx = 24, pady = 0, sticky = "nsew")

    # Create a frame as a container
    translate_container = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR, corner_radius = 8)
    translate_container.grid(row = 2, column = 0, padx = 120, pady = (24, 64), sticky = "nsew")
    translate_container.grid_columnconfigure(0, weight = 1)
    translate_container.grid_rowconfigure(1, weight = 1)

    frame.grid_rowconfigure(2, weight = 1)

    # Create a frame for the language selector
    lang_selector_frame = ctk.CTkFrame(translate_container, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    lang_selector_frame.grid(row = 0, column = 0, padx = 0, pady = (12, 0), sticky = "nsew")
    lang_selector_frame.grid_columnconfigure(0, weight = 1)
    lang_selector_frame.grid_columnconfigure(1, weight = 1)
    lang_selector_frame.grid_rowconfigure(0, weight = 1)

    # Initialize variables for language selection
    domain_var = ctk.StringVar(value = list(LANG.keys())[0])

    target_lang = list(LANG.keys())
    target_lang.pop(0)
    target_var = ctk.StringVar(value = target_lang[0])

    # Function to handle language changes
    def change_lang(box, role):
        global DOMAIN, TARGET

        if role == "domain":
            DOMAIN = box.get()
        elif role == "target":
            TARGET = box.get()
            
            translate()  # Start translating

    # Create a ComboBox for selecting the source language
    lang_domain_selector = ctk.CTkComboBox(lang_selector_frame, variable = domain_var, values = list(LANG.keys()), fg_color = main.SCROLLBAR_HOVER_COLOR,
                                           text_color = main.TEXT_COLOR, button_color = main.SCROLLBAR_HOVER_COLOR, button_hover_color = main.FADED_BORDER_COLOR,
                                           dropdown_fg_color = main.BASE_COLOR, dropdown_hover_color = main.ENTRY_COLOR, dropdown_text_color = main.TEXT_COLOR,
                                           border_width = 0, font = (main.FONT, 12, "normal"), dropdown_font = (main.FONT, 12, "normal"), justify = "center",
                                           corner_radius = 8, command = lambda event: change_lang(lang_domain_selector, "domain"))
    lang_domain_selector.grid(row = 0, column = 0, padx = (0, 6), pady = 0, sticky = "nsew")

    # Create a ComboBox for selecting the target language
    lang_target_selector = ctk.CTkComboBox(lang_selector_frame, variable = target_var, values = target_lang, fg_color = main.SCROLLBAR_HOVER_COLOR,
                                           text_color = main.TEXT_COLOR, button_color = main.SCROLLBAR_HOVER_COLOR, button_hover_color = main.FADED_BORDER_COLOR,
                                           dropdown_fg_color = main.BASE_COLOR, dropdown_hover_color = main.ENTRY_COLOR, dropdown_text_color = main.TEXT_COLOR,
                                           border_width = 0, font = (main.FONT, 12, "normal"), dropdown_font = (main.FONT, 12, "normal"), justify = "center",
                                           corner_radius = 8, command = lambda event: change_lang(lang_target_selector, "target"))
    lang_target_selector.grid(row = 0, column = 1, padx = (6, 0), pady = 0, sticky = "nsew")

    # Create a frame for input and output text boxes
    io_frame = ctk.CTkFrame(translate_container, fg_color = main.FRAME_COLOR, corner_radius = 8)
    io_frame.grid(row = 1, column = 0, padx = 0, pady = (12, 0), sticky = "nsew")
    io_frame.grid_columnconfigure(0, weight = 1)
    io_frame.grid_columnconfigure(1, weight = 1)
    io_frame.grid_rowconfigure(0, weight = 1)

    # Create the input text box
    input_box = ctk.CTkTextbox(io_frame, fg_color = main.BASE_COLOR, font = (main.FONT, 14, "normal"), text_color = main.TEXT_COLOR, 
                               scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                               corner_radius = 8)
    input_box.grid(row = 0, column = 0, padx = (0, 6), pady = 0, sticky = "nsew")
    input_box.configure(wrap = "word")

    # Create the output text box
    output_box = ctk.CTkTextbox(io_frame, fg_color = main.BASE_COLOR, font = (main.FONT, 14, "normal"), text_color = main.TEXT_COLOR, 
                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                                corner_radius = 8)
    output_box.grid(row = 0, column = 1, padx = (6, 0), pady = 0, sticky = "nsew")
    output_box.configure(state = "disabled", wrap = "word")
    
    # Function to get the values ​​from a text box and copy them to the clipboard
    def get_value(role):
        """
        Gets the values result from a text box and copy them to the clipboard.
        If the text box is empty, it displays an error message.
        """

        if role == "domain":
            value = input_box.get("1.0", "end-1c")
        elif role == "target":
            value = output_box.get("1.0", "end-1c")

        if value == "":
            popup.open_popup("No translation available", True)
        else:
            root.clipboard_clear()
            root.clipboard_append(value)

            popup.open_popup("Copied to clipboard", True)
            
    # Function to convert text to speech and play it
    def listen(text, role):        
        def listen_speech():
            # Dictionary mapping language names to their TTS language codes
            TTS_LANG = {"English" : "en",
                        "French" : "fr",
                        "Chinese" : "zh-CN",
                        "Portuguese" : "pt",
                        "Spanish" : "es"}
            
            # Determine the language based on the role
            if role == "domain":
                # Set language based on DOMAIN if it exists in TTS_LANG, otherwise default to English
                lang = TTS_LANG.get(DOMAIN, "en")
            elif role == "target":
                # Set language based on TARGET if it exists in TTS_LANG, otherwise default to English
                lang = TTS_LANG.get(TARGET, "en")
            
            # Check if the text is not empty
            if text:
                try:
                    # Convert text to speech and save to a temporary file
                    text_to_speech = gTTS(text = text, lang = lang)
                    path = getpath.base("temp/audio.mp3")
                    
                    # Save the audio file
                    text_to_speech.save(path)
                    
                    # Play the saved audio file
                    playsound.playsound(path)
                    
                    # Remove the temporary file after playing
                    if os.path.isfile(path):
                        os.remove(path)
                except PermissionError:
                    # Handle permission error if it occurs
                    if os.path.isfile(path):
                        os.remove(path)  # Remove the temporary file
            else:
                popup.open_popup("No translation available", True)
        
        # Create and start a new thread to run the say_text function
        thread = threading.Thread(target = listen_speech)
        
        thread.start()

    # Create a frame for the buttons
    buttons_frame = ctk.CTkFrame(translate_container, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    buttons_frame.grid(row = 2, column = 0, padx = 0, pady = (12, 12), sticky = "nsew")
    buttons_frame.grid_columnconfigure(0, weight = 1)
    buttons_frame.grid_columnconfigure(1, weight = 1)
    buttons_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame for the domain language buttons
    domain_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    domain_buttons_frame.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")
    domain_buttons_frame.grid_rowconfigure(0, weight = 1)
    
    # Create the "Listen" button for the domain language
    domain_listen_button = ctk.CTkButton(domain_buttons_frame, text = "Listen", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, 
                                      hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 24, width = 64, border_width = 0, 
                                      command = lambda: listen(input_box.get("1.0", "end-1c"), "domain"))
    domain_listen_button.grid(row = 0, column = 0, padx = (0, 4), pady = 0, sticky = "e")
    
    # Create the "Copy" button for the domain language
    domain_copy_button = ctk.CTkButton(domain_buttons_frame, text = "Copy", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, 
                                       hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 24, width = 64, border_width = 0, 
                                       command = lambda: get_value("domain"))
    domain_copy_button.grid(row = 0, column = 1, padx = (4, 0), pady = 0, sticky = "e")
    
    # Create a frame for the target language buttons
    target_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    target_buttons_frame.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "e")
    target_buttons_frame.grid_rowconfigure(0, weight = 1)
    
    # Create the "Listen" button for the target language
    target_listen_button = ctk.CTkButton(target_buttons_frame, text = "Listen", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, 
                                      hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 24, width = 64, border_width = 0, 
                                      command = lambda: listen(output_box.get("1.0", "end-1c"), "target"))
    target_listen_button.grid(row = 0, column = 0, padx = (12, 4), pady = 0, sticky = "e")
    
    # Create the "Copy" button for the target language
    target_copy_button = ctk.CTkButton(target_buttons_frame, text = "Copy", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, 
                                       hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 24, width = 64, border_width = 0, 
                                       command = lambda: get_value("target"))
    target_copy_button.grid(row = 0, column = 1, padx = (4, 0), pady = 0, sticky = "e")
    
    global FRAME
    
    FRAME = frame  # Assign the frame to the global variable FRAME

    # Function to translate the text
    def translate(event = None): 
        """
        This function is used to start translating a text into another language.
        """
        
        def check_internet_connection(url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'do_translate' function.
            If the connection fails, it will show a popup message to check the internet connection.

            param url: URL used to check the internet connection. Default is http://www.google.com/
            """
            
            # Function to translate languages
            def do_translate():
                # Check if frame is destroyed if 
                if is_widget.is_exist(FRAME): 
                    return  # If the frame is destroyed, exit the function
        
                text = input_box.get("1.0", tk.END)

                translator = GoogleTranslator(source = LANG[DOMAIN], target = LANG[TARGET])
                translation = translator.translate(text)

                cur_translation = output_box.get("1.0", tk.END).strip()

                if translation != cur_translation:
                    output_box.configure(state = "normal")
                    output_box.delete("1.0", tk.END)
                    output_box.insert(tk.END, translation)
                    output_box.configure(state = "disabled")

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'do_translate' function
                    thread = threading.Thread(target = do_translate)

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Create and start a new thread to check the internet connection and start the translation process
        thread = threading.Thread(target = check_internet_connection)
        
        thread.start()

    # Bind the translate function to the KeyRelease event on the input box
    input_box.bind("<KeyRelease>", translate)
