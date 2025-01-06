# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import threading
import requests
import os
import cleaner
import main
import flassencia
import is_widget
import getpath
import popup

# Supported language dictionary
LANG = {"Dutch" : "dutch",
        "English" : "english",
        "French" : "french",
        "German" : "german",
        "Indonesian" : "indonesian",
        "Italian" : "italian",
        "Portuguese" : "portuguese",
        "Spanish" : "spanish"}

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Variable to control loading animation state
ANIM = False

# Function to open the Flassencia frame
def flassencia_tool(root, frame):
    """
    This function initializes the flassencia tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the flassencia tool interface
    """
    
    global LAST_PRESSED, ANIM
    
    # Resets variable values
    LAST_PRESSED = None
    ANIM =  False
    
    # Clean specific files using the cleaner module
    cleaner.clean_file()
    
    # Reset the cursor icon
    if root.cget("cursor") != "arrow":
        root.configure(cursor = "arrow")

    # Destroy the existing frame
    frame.destroy()

    # Create a new frame with specified width, height, and background color
    frame = ctk.CTkFrame(root, width = 800, height = 640, fg_color = main.FRAME_COLOR)

    # Position the new frame within the root window grid
    frame.grid(row = 0, column = 1, padx = (8, 16), pady = 16, sticky = "nsew")
        
    # Configure the column of the new frame to expand with available space
    frame.grid_columnconfigure(0, weight = 1)

    # Add a label for the flassencia tool frame
    flassencia_label = ctk.CTkLabel(frame, text = "Flassencia", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    flassencia_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")
    
    # Function to handle when typing starts
    def on_type(event):
        if input_box.get("1.0", tk.END).strip() == "Type something":
            # Delete all text in the textbox
            input_box.delete("1.0", tk.END)
            
            # Change text color to main text color
            input_box.configure(text_color = main.TEXT_COLOR)
            
    # Function to handle when the textbox loses focus
    def on_focus_out(event):
        if input_box.get("1.0", tk.END).strip() == "":
            # Insert the text "Type something" in the textbox
            input_box.insert(tk.END, "Type something")
            
            # Change text color to faded text color
            input_box.configure(text_color = main.FADED_TEXT_COLOR)
    
    # Create an input textbox
    input_box = ctk.CTkTextbox(frame, height = 160, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.FADED_TEXT_COLOR, 
                               scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                               border_width = 2, border_color = main.FADED_BORDER_COLOR, corner_radius = 8)
    input_box.grid(row = 1, column = 0, padx = 120, pady = (32, 12), sticky = "nsew")
    input_box.configure(wrap = "word")
    input_box.insert(tk.END, "Type something")
    
    # Bind events to the textbox widget
    input_box.bind("<FocusIn>", on_type)  # Bind FocusIn event to on_type function
    input_box.bind("<FocusOut>", on_focus_out)  # Bind FocusOut event to on_focus_out function
    
    # Extension selection frames and canvases
    lang_selection_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR) 
    lang_selection_frame.grid(row = 2, column = 0, padx = 160, pady = 4, sticky = "nsew") 
    lang_selection_frame.grid_columnconfigure(0, weight = 1)

    lang_selection_canvas = ctk.CTkCanvas(lang_selection_frame, height = 28) 
    lang_selection_canvas.grid(row = 0, column = 0, sticky = "nsew") 
    lang_selection_canvas.grid_columnconfigure(0, weight = 1)

    lang_button_frame = ctk.CTkFrame(lang_selection_canvas, height = 28, fg_color = main.FRAME_COLOR) 
    lang_button_frame.grid(row = 0, column = 0, sticky = "nsew") 

    # Horizontal scrollbar 
    scrollbar = ctk.CTkScrollbar(lang_selection_frame, orientation = "horizontal", command = lang_selection_canvas.xview, height = 12,
                                    button_color = main.SCROLLBAR_COLOR, button_hover_color = main.SCROLLBAR_HOVER_COLOR) 
    scrollbar.grid(row = 1, column = 0, sticky = "nsew") 
    
    # Configure canvas for scrollbar 
    lang_selection_canvas.configure(xscrollcommand = scrollbar.set) 
    lang_selection_canvas.create_window((0, 0), window = lang_button_frame, anchor = "nw") 
    
    # Update scroll region when the frame size changes 
    lang_button_frame.bind("<Configure>", lambda e: lang_selection_canvas.configure(scrollregion = lang_selection_canvas.bbox("all")))
    
    lang_path = getpath.base("bin/log/lang_log.bin")
    
    # Function to change the color of the pressed button
    def change_button_color(button):
        global LAST_PRESSED

        # If there is a previously pressed button, reset its color
        if LAST_PRESSED is not None:
            LAST_PRESSED.configure(fg_color = main.BASE_COLOR, hover_color = main.ENTRY_COLOR, text_color = main.FADED_LABEL_COLOR, 
                                    border_width = 1, border_color = main.BORDER_COLOR)

        # Change the color of the currently pressed button
        button.configure(fg_color = main.FG_COLOR, hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR,
                        border_width = 0, border_color = main.FRAME_COLOR)
        
        # Update the last pressed button to the current button
        LAST_PRESSED = button
        
    # Function to handle language selection
    def lang(event, button):
        button_name = button.cget("text")

        # Write the language code to the file
        with open(lang_path, "wb") as file:
            if button_name in sorted(list(LANG.keys())):
                lang_code = LANG[button_name]
                
                file.write(lang_code.encode("utf-8"))

    # Function to create a language selection button
    def lang_button(text, row, column, frame):
        button = ctk.CTkButton(frame, text = text, font = (main.FONT, 10, "bold"), border_color = main.BORDER_COLOR, 
                                text_color = main.FADED_LABEL_COLOR, fg_color = main.BASE_COLOR, height = 24, width = 86,
                                border_width = 1, hover_color = main.ENTRY_COLOR, command = lambda: change_button_color(button))
        button.grid(row = 0, column = column, padx = 4, pady = 4, sticky = "nsew")
        button.bind("<Button-1>", lambda event: lang(event, button))  # Bind the button click event to lang function

        return button
    
    # Loop through sorted LANG keys and create a button for each language
    for index, language in enumerate(sorted(list(LANG.keys()))): 
        lang_button(language, 0, index, lang_button_frame)
    
    # Frame for summarizing
    summarize_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR) 
    summarize_frame.grid(row = 3, column = 0, padx = 0, pady = 4, sticky = "n") 
    summarize_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame for the output box and copy button
    output_frame = ctk.CTkFrame(frame, height = 160, fg_color = main.FRAME_COLOR, border_width = 2, border_color = main.FADED_BORDER_COLOR, 
                                corner_radius = 8) 
    output_frame.grid(row = 4, column = 0, padx = 120, pady = (12, 32), sticky = "nsew")
    output_frame.grid_columnconfigure(0, weight = 1)
    output_frame.grid_rowconfigure(0, weight = 1)
    
    # Label to display the transcription progress
    loading_label = ctk.CTkLabel(output_frame, text = "Summerizing", font = (main.FONT, 16, "bold"), text_color = main.FADED_LABEL_COLOR) 
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

        # Show the label
        loading_label.grid(row = 0, column = 0, padx = 12, pady = 24, sticky = "nsew") 
        
        animate_loading(loading_label, "Summerizing")

    # Function to stop the loading animation
    def stop_animation(): 
        global ANIM
        
        ANIM = False
        
        # Hide the label
        loading_label.grid_forget()
        loading_label.configure(text = "Summerizing")
    
    length_var = tk.StringVar()
    length_var.set("Text length")  # Set default value for length_var
    
    # Function to handle when typing starts
    def on_type_entry(event):
        if length_var.get().strip() == "Text length":
            # Delete all text in the entry
            length_entry.delete(0, tk.END)
            
            # Change text color to main text color
            length_entry.configure(text_color = main.TEXT_COLOR)
            
    # Function to handle when the entry loses focus
    def on_focus_out_entry(event):
        if length_var.get().strip() == "":
            # Insert the text "Text length" in the entry
            length_var.set("Text length")
            
            # Change text color to faded text color
            length_entry.configure(text_color = main.FADED_TEXT_COLOR)
    
    # Create an entry widget with a placeholder text
    length_entry = ctk.CTkEntry(summarize_frame, textvariable = length_var, width = 86, height = 28, fg_color = main.BASE_COLOR, 
                                font = (main.FONT, 12, "normal"), corner_radius = 8, text_color = main.FADED_TEXT_COLOR, border_color = main.BORDER_COLOR, 
                                border_width = 1)
    length_entry.grid(row = 0, column = 0, padx = 0, pady = 4, sticky = "nsew")
    
    # Bind events to the entry widget
    length_entry.bind("<FocusIn>", on_type_entry)  # Bind FocusIn event to on_type_entry function
    length_entry.bind("<FocusOut>", on_focus_out_entry)  # Bind FocusOut event to on_focus_out_entry function
    
    # Function to summarize the input text
    def summary(frame):
        start_animation()
        
        output_box.grid_forget()
        copy_button_frame.grid_forget()
        
        def run_summary(frame):
            input_text = input_box.get("1.0", tk.END).strip()  # Get the text from the input box
            
            # Read the language code from the file
            with open(lang_path, "rb") as file:
                lang_code = file.read().decode("utf-8")
                
            length = length_var.get().strip()  # Get the length from the entry
            
            # Check if any of the input fields are empty or contain placeholder text
            if (input_text == "" or input_text == "Type something") or (lang_code == "") or (length == "" or length == "Text length"):
                popup.open_popup("Please fill in the text box, select the language,\nand enter the text length", True)
                
                return
            else:
                # Call the summarization function
                results = flassencia.flassencia(frame, input_text, lang_code, length)
                
                output_box.configure(state = "normal")
                output_box.insert(tk.END, results)  # Insert the results into the output box
                output_box.configure(state = "disabled")
                
            output_box.grid(row = 0, column = 0, padx = 12, pady = (12, 8), sticky = "nsew")
            copy_button_frame.grid(row = 1, column = 0, padx = 12, pady = (0, 12), sticky = "e")
            
            stop_animation()
        
        # Run the summarization in a separate thread
        thread = threading.Thread(target = run_summary, args = (frame,))
        
        thread.start()
    
    def run_flassencia(frame):
        """
        Start the process of summarizing text in a separate thread to avoid GUI blocking.
        """

        def check_internet_connection(frame, url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'summary' function.
            If the connection fails, it will show a popup message to check the internet connection.
            
            :param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'summary' function
                    thread = threading.Thread(target = summary, args = (frame,))

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Call the function to check the internet connection
        check_internet_connection(frame)
    
    # Create a button to start the summarization process
    summarize_button = ctk.CTkButton(summarize_frame, text = "Summarize", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                                     hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 100, command = lambda: run_flassencia(frame))
    summarize_button.grid(row = 0, column = 1, padx = (8, 0), pady = 4, sticky = "nsew")
    
    frame.grid_rowconfigure(4, weight = 1)
    
    # Bind the Enter key to run_flassencia function
    length_entry.bind("<Return>", lambda event: run_flassencia(frame))
    
    # Create an output textbox to display the results
    output_box = ctk.CTkTextbox(output_frame, height = 160, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR,
                                border_width = 0, corner_radius = 8)
    output_box.grid(row = 0, column = 0, padx = 12, pady = (12, 8), sticky = "nsew")
    output_box.configure(state = "disabled", wrap = "word")  # Disable editing in the output box
    
    # Create a frame for the copy button
    copy_button_frame = ctk.CTkFrame(output_frame, height = 24, fg_color = main.FRAME_COLOR, border_width = 2, border_color = main.FADED_BORDER_COLOR, 
                                     corner_radius = 8) 
    copy_button_frame.grid(row = 1, column = 0, padx = 12, pady = (0, 12), sticky = "e")
    copy_button_frame.grid_rowconfigure(0, weight = 1)
    
    # Function to get the value from the output box and copy it to the clipboard
    def get_value():
        """
        Gets the results from the output box and copies it to the clipboard.
        If the output box is empty, it displays an error message.
        """
            
        # Get the text from the output box and copy it to the clipboard
        results = output_box.get("1.0", tk.END).strip()
        
        if results == "":
            # If empty, open a popup to indicate no results is available
            popup.open_popup("No results available", True)
        else:
            root.clipboard_clear()  # Clear the current clipboard content
            root.clipboard_append(results)  # Append the results to the clipboard

            # Open a popup to indicate the results has been copied to the clipboard
            popup.open_popup("Copied to clipboard", True)
    
    # Create the copy button within the copy button frame
    copy_button = ctk.CTkButton(copy_button_frame, text = "Copy", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, height = 24, command = get_value)
    copy_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")
    
    # Get the current children of the frame
    is_widget.WIDGETS = frame.winfo_children()
    