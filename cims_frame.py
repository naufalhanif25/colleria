# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import threading
import requests
import os
import cleaner
import main
import is_widget
import getpath
import popup
import cims

# Function to open the CIMS frame
def cims_tool(root, frame):
    """
    This function initializes the cims tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the cims tool interface
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

    # Add a label for the cims tool frame
    cims_label = ctk.CTkLabel(frame, text = "CIMS", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    cims_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")
    
    # Create and configure the input frame for user inputs
    input_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR, border_width = 2, border_color = main.FADED_BORDER_COLOR, corner_radius = 16)
    input_frame.grid(row = 1, column = 0, padx = 32, pady = (36, 16), sticky = "nsew")
    input_frame.grid_columnconfigure(0, weight = 1)
    input_frame.grid_rowconfigure(1, weight = 1)
    
    # Create and configure the button frame within the input frame
    input_button_frame = ctk.CTkFrame(input_frame, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    input_button_frame.grid(row = 0, column = 0, padx = 12, pady = (12, 0), sticky = "nsew")
    input_button_frame.grid_columnconfigure(0, weight = 1)
    input_button_frame.grid_rowconfigure(1, weight = 1)
    
    # Function to run CIMS interpreter
    def run():
        """ 
        This function runs the CIMS interpreter with the provided scripts from the input box. 
        It reads the scripts line by line, executes them, and displays the results in the output box. 
        """
        
        # Retrieve the scripts from the input box
        scripts = input_box.get("1.0", "end-1c")
        
        # Check if there are any scripts to run
        if scripts == "" or scripts == "Write a script or write '$command help' to read the manual":
            popup.open_popup("There are no scripts to run", True)
        else:
            # Create a new CIMS object with the script and line number
            cims_obj = cims.CIMS(scripts)
            
            cims_obj.run()  # Run the CIMS object
            
            result = cims_obj.call()  # Call the CIMS object to get the result
            
            # Enable the output box for editing
            output_box.configure(state = "normal")
            
            # Insert the result into the output box
            output_box.insert(tk.END, result)
            
            # Disable the output box to prevent further editing
            output_box.configure(state = "disabled")
            
            # Add a newline at the end of the output
            output_box.configure(state = "normal")
            output_box.insert(tk.END, "\n")
            output_box.configure(state = "disabled")
    
    # Create and configure the run button to execute the run function
    run_button = ctk.CTkButton(input_button_frame, text = "Run  ▶", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                               hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 68, height = 24,
                               command = run)
    run_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")
    
    # Function to handle when typing starts
    def on_type(event):
        if input_box.get("1.0", tk.END).strip() == "Write a script or write '$command help' to read the manual":
            # Delete all text in the textbox
            input_box.delete("1.0", tk.END)
            
            # Change text color to main text color
            input_box.configure(text_color = main.TEXT_COLOR)
            
    # Function to handle when the textbox loses focus
    def on_focus_out(event):
        if input_box.get("1.0", tk.END).strip() == "":
            # Insert the text "Write a script or write '$command help' to read the manual" in the textbox
            input_box.insert(tk.END, "Write a script or write '$command help' to read the manual")
            
            # Change text color to faded text color
            input_box.configure(text_color = main.FADED_TEXT_COLOR)
    
    # Create and configure the input text box for user script inputs
    input_box = ctk.CTkTextbox(input_frame, font = ("Consolas", 12, "normal"), text_color = main.FADED_TEXT_COLOR, fg_color = main.BASE_COLOR, 
                               corner_radius = 8, scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
    input_box.grid(row = 1, column = 0, padx = 12, pady = (8, 12), sticky = "nsew")
    input_box.configure(wrap = "word")
    input_box.insert(tk.END, "Write a script or write '$command help' to read the manual")
    
    # Bind events to the textbox widget
    input_box.bind("<FocusIn>", on_type)  # Bind FocusIn event to on_type function
    input_box.bind("<FocusOut>", on_focus_out)  # Bind FocusOut event to on_focus_out function
    
    # Configure the grid rows of the main frame to expand with available space
    frame.grid_rowconfigure(1, weight = 1)
    frame.grid_rowconfigure(2, weight = 1)
    
    # Create and configure the output frame for displaying results
    output_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR, border_width = 2, border_color = main.FADED_BORDER_COLOR, corner_radius = 16)
    output_frame.grid(row = 2, column = 0, padx = 32, pady = (0, 32), sticky = "nsew")
    output_frame.grid_columnconfigure(0, weight = 1)
    output_frame.grid_rowconfigure(1, weight = 1)
    
    # Create and configure the output button frame within the output frame
    output_button_frame = ctk.CTkFrame(output_frame, fg_color = main.FRAME_COLOR, height = 32, corner_radius = 8)
    output_button_frame.grid(row = 0, column = 0, padx = 12, pady = (12, 0), sticky = "nsew")
    output_button_frame.grid_columnconfigure(0, weight = 1)
    output_button_frame.grid_rowconfigure(1, weight = 1)
    
    # Function to clear the entire console
    def clear_console():
        # Check if there are any console contents to clear
        if output_box.get("1.0", "end-1c") == "":
            popup.open_popup("There are no console contents to clean", True)
        else:
            output_box.configure(state = "normal")
            output_box.delete("1.0", tk.END)
            output_box.configure(state = "disabled")
    
    # Create and configure the clear button to execute the clear_console function
    clear_button = ctk.CTkButton(output_button_frame, text = "Clear", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                                 hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 68, height = 24,
                                 command = clear_console)
    clear_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")
    
    # Create and configure the output text box for displaying results of the executed scripts
    output_box = ctk.CTkTextbox(output_frame, font = ("Consolas", 12, "normal"), fg_color = main.BASE_COLOR, corner_radius = 8,
                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
    output_box.grid(row = 1, column = 0, padx = 12, pady = 12, sticky = "nsew")
    output_box.configure(state = "disabled", wrap = "word")
    