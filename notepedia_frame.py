# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import popup
import main
import cleaner
import is_widget

# Global variables to manage the state of the note
TITLE = "Untitled"
PATH = ""
NOTES = ""
CHANGE = False

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

    global TITLE, PATH, NOTES, CHANGE

    # Resets variable values
    TITLE = "Untitled"
    PATH = ""
    NOTES = ""
    CHANGE = False

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
    container.grid(row = 1, column = 0, padx = 16, pady = (0, 16), sticky = "nsew")
    container.grid_columnconfigure(0, weight = 1)
    container.grid_rowconfigure(1, weight = 1)

    # Create a header frame inside the container
    header_frame = ctk.CTkFrame(container, height = 32, fg_color = main.FRAME_COLOR, corner_radius = 8)
    header_frame.grid(row = 0, column = 0, padx = 8, pady = (0, 4), sticky = "nsew")
    header_frame.grid_columnconfigure(0, weight = 1)
    header_frame.grid_rowconfigure(0, weight = 1)

    # Create a frame for buttons inside the header
    buttons_frame = ctk.CTkFrame(header_frame, width = 120, height = 32, fg_color = main.FRAME_COLOR, corner_radius = 8)
    buttons_frame.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "e")

    # Create a frame for the filename label
    filename_frame = ctk.CTkFrame(header_frame, fg_color = main.FRAME_COLOR, corner_radius = 8)
    filename_frame.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
    filename_frame.grid_rowconfigure(0, weight = 1)

    # Create message log label
    filename_label = ctk.CTkLabel(filename_frame, text = TITLE, font = (main.FONT, 16, "bold"), text_color = main.FADED_LABEL_COLOR, anchor = "w") 
    filename_label.grid(row = 0, column = 0, padx = 0, pady = (4, 0), sticky = "nsew") 

    # Function to create a new note
    def new_note():
        """ 
        This function creates a new note by resetting
        the title and the content of the notepad. 
        """

        global TITLE, CHANGE

        if not CHANGE:
            TITLE = "Untitled"  # Change the title to Untitled

            filename_label.configure(text = TITLE)  # Reset file name label
            notepad_box.delete("1.0", tk.END)  # Reset the notepad box

            CHANGE = False  # Resets the change variable to false
        else:
            # Open popup
            popup.open_popup("Please save your notes first before creating a new note", True)

    # Function to open a text file (note)
    def open_note():
        """ 
        This function opens an existing note by loading 
        its content from a file selected by the user. 
        """

        global TITLE, NOTES, PATH, CHANGE

        if not CHANGE:
            # Opening the path with the file manager
            PATH = filedialog.askopenfilename(defaultextension = ".txt",
                                              filetypes = [("Text files", "*.txt"), 
                                                           ("All files", "*.*")],
                                              title = "Select a note")

            if PATH != "":
                # Reads the contents of a text file
                with open(PATH, "r", encoding = "utf-8") as file:
                    content = file.read()

                # Change the values ​​of variables
                lines = content.splitlines()
                TITLE = lines[0]
                NOTES = "\n".join(lines[1:])
                CHANGE = False

            # Update file name label and notepad box
            filename_label.configure(text = TITLE)
            notepad_box.delete("1.0", tk.END)
            notepad_box.insert(tk.END, NOTES)
        else:
            # Open popup
            popup.open_popup("Please save your notes first before opening existing notes", True)

    # Function to save a note
    def save_note():
        """ 
        This function saves the current note to a file. 
        If the note has not been saved before, 
        it prompts the user to select a file path. 
        """

        global TITLE, NOTES, PATH, CHANGE

        if PATH != "" and os.path.exists(PATH) == True:
            # Change the values ​​of variable
            notes = notepad_box.get("1.0", tk.END)
            title = os.path.basename(PATH)
            title = title.replace("*", "")

            # Updates the contents of a text file
            with open(PATH, "w") as file:
                file.write(title + "\n")
                file.write(notes)
        else:
            # Opening the path with the file manager
            PATH = filedialog.asksaveasfilename(defaultextension = ".txt",
                                                filetypes = [("Text files", "*.txt"),
                                                             ("All files", "*.*")],
                                                title = "Save notes")

            # Change the values ​​of variable
            notes = notepad_box.get("1.0", tk.END)
            title = os.path.basename(PATH)
            title = title.replace("*", "")

        if PATH != "":
            # Updates the contents of a text file
            with open(PATH, "w") as file:
                file.write(title + "\n")
                file.write(notes)

            # Reads the contents of a text file
            with open(PATH, "r", encoding = "utf-8") as file:
                content = file.read()

            # Change the values ​​of variables
            lines = content.splitlines()
            TITLE = lines[0]
            NOTES = "\n".join(lines[1:])
            CHANGE = False

        # Update file name label and notepad box
        filename_label.configure(text = TITLE)
        notepad_box.delete("1.0", tk.END)
        notepad_box.insert(tk.END, NOTES)
    
    # Define buttons and their corresponding commands
    buttons = ["New", "open", "Save"]
    commands = [new_note, open_note, save_note]

    # Create buttons and add them to the buttons frame
    for index, (button_name, command) in enumerate(zip(buttons, commands)):
        if index == 0 or index == len(buttons) - 1:
            padx = 0
        else:
            padx = 8

        button = ctk.CTkButton(buttons_frame, text = button_name, font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                               hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, command = command)
        button.grid(row = 0, column = index, padx = padx, pady = 8, sticky = "nsew")

    # Create the notepad text box
    notepad_box = ctk.CTkTextbox(container, fg_color = main.BASE_COLOR, font = (main.FONT, 14, "normal"), text_color = main.TEXT_COLOR, 
                                 scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                                 corner_radius = 8)
    notepad_box.grid(row = 1, column = 0, padx = 8, pady = (0, 8), sticky = "nsew")
    notepad_box.configure(wrap = "word")
    notepad_box.insert(tk.END, NOTES)

    # Function to update the filename label
    def update_title(event): 
        """ 
        This function updates the title with an asterisk (*) 
        if the content of the notepad has changed since 
        the last save. 
        """

        global CHANGE

        # Gets the value of the notepad box
        cur_notes = notepad_box.get("1.0", tk.END).strip() 

        if cur_notes != NOTES: 
            CHANGE = True  # Update the change variable to false

            # Update the title with an asterisk (*)
            filename_label.configure(text = TITLE + "*") 
        else:
            CHANGE = False  # Resets the change variable to false

            # Update the title without an asterisk (*)
            filename_label.configure(text = TITLE) 
    
    # Bind the update_title function to the KeyRelease event
    notepad_box.bind("<KeyRelease>", update_title)

    # Get the current children of the frame
    is_widget.WIDGETS = frame.winfo_children()
