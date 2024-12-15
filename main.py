# Importing necessary libraries and modules
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import notepedia_frame as npf
import doclab_frame as dlf
import transcriberia_frame as tf
import researcheria_frame as rf
import aboutus_popup
import os
import cleaner
import webbrowser

# Language options available for transcription
LANG = {"Afrikaans" : "af-ZA",
        "Arabic" : "ar-SA",
        "Chinese" : "cmn-Hans-CN",
        "Dutch" : "nl-NL",
        "English (US)" : "en-US", 
        "English (UK)" : "en-GB", 
        "French" : "fr-FR", 
        "German" : "de-DE",
        "Hindi" : "hi-IN",
        "Indonesian" : "id-ID", 
        "Italian" : "it-IT", 
        "Japanese" : "ja-JP",
        "Javanese" : "jv-ID", 
        "Korean" : "ko-KR", 
        "Malaysia" : "ms-MY",
        "Portuguese" : "pt-PT", 
        "Russian" : "ru-RU", 
        "Spanish" : "es-ES",
        "Sundanese" : "su-ID",
        "Thai" : "th-TH",
        "Turkish" : "tr-TR",
        "Vietnamese" : "vi-VN"}

# Color constants for the application interface
BASE_COLOR = "#FFFFFF"
FRAME_COLOR = "#F1F2F6"
FG_COLOR = "#70A1FF"
FG_HOVER_COLOR = "#1E90FF"
BORDER_COLOR = "#70A1FF"
FADED_TEXT_COLOR = "#70A1FF"
FADED_LABEL_COLOR = "#747D8C"
ENTRY_COLOR = "#DFE4EA"
TEXT_COLOR = "#2F3542"
SCROLLBAR_COLOR = "#dfe4ea"
SCROLLBAR_HOVER_COLOR = "#ced6e0"

LAST_PRESSED = None # Variable to keep track of the last pressed button

"""
This main code is a combination of all modules.
All frames and algorithms come together here.
"""

if __name__ == "__main__":
    # Clean specific files at the start
    cleaner.clean_file()
    
    # Initialize the main application window with drag-and-drop functionality
    root = TkinterDnD.Tk()
    root.configure(bg = BASE_COLOR)
    root.iconbitmap("public/colleria.ico")
    root.title("Colleria")
    # root.resizable(False, False)

    # Set the dimensions and position of the application window
    width = 1080
    height = 640

    x_pos = int((root.winfo_screenwidth() / 2) - (width / 2))
    y_pos = int((root.winfo_screenheight() / 2) - (height / 2))
    
    root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    # Create the left panel frame to hold the frames
    left_panel_frame = ctk.CTkFrame(root, width = 164, height = 640, fg_color = BASE_COLOR)
    left_panel_frame.grid(row = 0, column = 0, padx = (16, 8), pady = 16, sticky = "nsew")
    left_panel_frame.grid_columnconfigure(0, weight = 1)
    left_panel_frame.grid_rowconfigure(0, weight = 1)

    # Create a frame for the tool list on the left panel frame
    toollist_frame = ctk.CTkFrame(left_panel_frame, width = 164, height = 640, fg_color = FRAME_COLOR)
    toollist_frame.grid(row = 0, column = 0, padx = 0, pady = (0, 8), sticky = "nsew")
    toollist_frame.grid_columnconfigure(0, weight = 1)
    toollist_frame.grid_rowconfigure(0, weight = 1)

    toollist_canvas = ctk.CTkCanvas(toollist_frame, width = 164, height = 636) 
    toollist_canvas.grid(row = 0, column = 0, sticky = "nsew") 
    toollist_canvas.grid_columnconfigure(0, weight = 1)

    toollist_button_frame = ctk.CTkFrame(toollist_canvas, width = 152, height = 636, fg_color = FRAME_COLOR) 
    toollist_button_frame.grid(row = 0, column = 0, sticky = "nsew") 

    scrollbar = ctk.CTkScrollbar(toollist_frame, orientation = "vertical", command = toollist_canvas.yview, width = 12,
                                 button_color = SCROLLBAR_COLOR, button_hover_color = SCROLLBAR_HOVER_COLOR) 
    scrollbar.grid(row = 0, column = 1, padx = 4, pady = 8, sticky = "nsew") 

    # Configure canvas for scrollbar 
    toollist_canvas.configure(yscrollcommand = scrollbar.set) 
    toollist_canvas.create_window((0, 0), window = toollist_button_frame, anchor = "nw")

    # Update scroll region when the frame size changes 
    toollist_button_frame.bind("<Configure>", lambda e: toollist_canvas.configure(scrollregion = toollist_canvas.bbox("all")))

    # Create a frame to hold the other buttons
    other_frame = ctk.CTkFrame(left_panel_frame, width = 164, height = 120, fg_color = FRAME_COLOR)
    other_frame.grid(row = 1, column = 0, padx = 0, pady = (8, 0), sticky = "nsew")
    other_frame.grid_columnconfigure(0, weight = 1)

    # Create a frame for the tool content on the right side
    tool_frame = ctk.CTkFrame(root, width = 760, height = 640, fg_color = FRAME_COLOR)
    tool_frame.grid(row = 0, column = 1, padx = (8, 16), pady = 16, sticky = "nsew")
    tool_frame.grid_columnconfigure(0, weight = 1)

    # Label for the tool list
    menu_label = ctk.CTkLabel(toollist_button_frame, text = "Tool List", font = ("Arial", 16, "bold"), anchor = "w",
                              text_color = TEXT_COLOR)
    menu_label.grid(row = 0, column = 0, padx = 12, pady = 6, sticky = "nsew")

    # Function to change the color of the pressed button
    def change_button_color(button):
        global LAST_PRESSED

        # If there is a previously pressed button, reset its color
        if LAST_PRESSED is not None:
            LAST_PRESSED.configure(fg_color = FG_COLOR, hover_color = FG_HOVER_COLOR, text_color = BASE_COLOR,
                                   border_width = 0, border_color = FRAME_COLOR)

        # Change the color of the currently pressed button
        button.configure(fg_color = FRAME_COLOR, hover_color = ENTRY_COLOR, text_color = FADED_TEXT_COLOR, 
                         border_width = 2, border_color = BORDER_COLOR)
        
        # Update the last pressed button to the current button
        LAST_PRESSED = button

    # Create the toollist buttons and commands
    buttons = ["Notepedia", "DocLab", "Transcriberia", "Researcheria"]
    commands = [lambda: npf.notepedia_tool(root, tool_frame),
                lambda: dlf.doclab_tool(root, tool_frame),
                lambda: tf.transcriber_tool(root, tool_frame), 
                lambda: rf.researcheria_tool(root, tool_frame)]

    for row, (button_text, command) in enumerate(zip(buttons, commands)):
        button = ctk.CTkButton(toollist_button_frame, text = button_text, font = ("Arial", 12, "bold"), fg_color = FG_COLOR, 
                               hover_color = FG_HOVER_COLOR, text_color = BASE_COLOR, height = 32, width = 154,
                               command = command)
        button.grid(row = row + 1, column = 0, padx = 12, pady = 4, sticky = "nsew")
        button.bind("<Button-1>", lambda event, button = button: change_button_color(button))

        toollist_button_frame.grid_columnconfigure(row + 1, weight = 1)

    # Create the other buttons
    other_buttons = ["Donate", "About us"]
    commands = [lambda: webbrowser.open_new_tab("https://github.com/naufalhanif25"),
               aboutus_popup.open_popup]
    
    for row, (button_text, command) in enumerate(zip(other_buttons, commands)):
        if row == 0:
            pady = (16, 4)
        elif row == (len(other_buttons) - 1):
            pady = (4, 16)
        else:
            pady = 4

        button = ctk.CTkButton(other_frame, text = button_text, font = ("Arial", 12, "bold"), fg_color = FG_COLOR, 
                               hover_color = FG_HOVER_COLOR, text_color = BASE_COLOR, height = 32, width = 154,
                               command = command)
        button.grid(row = row + 1, column = 0, padx = 12, pady = pady, sticky = "nsew")

    # Configure the grid layout for the main application window
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 1) 

    # Start the main event loop to display the application window
    root.mainloop()

    # Clean specific files at the end
    cleaner.clean_file()
