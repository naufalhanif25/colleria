# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import main
import cleaner
import colleriaai
import threading
import popup
import requests

PROMPT = None  # To store the current prompt
ANIM = False  # To control loading animation state

# Function to open the Notepedia frame
def colleriaai_tool(root, frame):
    """
    This function initializes the colleria ai tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 
    
    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the colleria ai tool interface
    """

    global PROMPT, ANIM

    # Resets variable values
    PROMPT = None
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

    # Add a label for the colleria ai tool frame
    colleriaai_label = ctk.CTkLabel(frame, text = "Colleria.AI", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    colleriaai_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")

    model_label = ctk.CTkLabel(frame, text = colleriaai.MODEL_NAME, font = (main.FONT, 12, "bold"), text_color = main.TEXT_COLOR)
    model_label.grid(row = 1, column = 0, padx = 24, pady = (0, 16), sticky = "nsew")

    # Create a frame for the response textbox
    response_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
    response_frame.grid(row = 2, column = 0, padx = 160, pady = (8, 2), sticky = "nsew")
    response_frame.grid_columnconfigure(0, weight = 1)
    response_frame.grid_rowconfigure(0, weight = 1)

    frame.grid_rowconfigure(2, weight = 1)

    # Create a frame for the prompt entry and button
    prompt_frame = ctk.CTkFrame(frame, height = 64, fg_color = main.FRAME_COLOR)
    prompt_frame.grid(row = 4, column = 0, padx = 160, pady = (0, 24), sticky = "nsew")
    prompt_frame.grid_columnconfigure(0, weight = 1)
    prompt_frame.grid_rowconfigure(0, weight = 1)

    # Create a text variable for the search entry and set a placeholder text
    prompt_var = tk.StringVar() 
    prompt_var.set("Ask Colleria.AI")

    # Textbox to display the response
    response_box = ctk.CTkTextbox(response_frame, fg_color = main.FRAME_COLOR, font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR, 
                                  scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
    response_box.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
    response_box.configure(state = "disabled")

    # Create a loading label to show the loading animation
    loading_label = ctk.CTkLabel(response_frame, text = "Let me think for a moment", font = (main.FONT, 12, "normal"), 
                                 text_color = main.FADED_LABEL_COLOR)
    loading_label.grid(row = 0, column = 0, padx = 0, pady = (0, 320), sticky = "nsew")
    loading_label.grid_forget()  # Hide the label initially

    # Create a button frame to hold the copy button
    button_frame = ctk.CTkFrame(frame, height = 28, fg_color = main.FRAME_COLOR)
    button_frame.grid(row = 3, column = 0, padx = 160, pady = (2, 12), sticky = "e")
    button_frame.grid_forget()
    button_frame.grid_rowconfigure(0, weight = 1)

    # Function to handle entry click (focus in)
    def on_entry_click(event): 
        if prompt_var.get() == "Ask Colleria.AI": 
            prompt_entry.configure(text_color = main.TEXT_COLOR)
            prompt_var.set("") 

    # Function to handle entry focus out
    def on_focus_out(event): 
        if prompt_var.get() == "": 
            prompt_entry.configure(text_color = main.FADED_LABEL_COLOR)
            prompt_var.set("Ask Colleria.AI")

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

        animate_loading(loading_label, "Let me think for a moment")

    # Function to stop the loading animation
    def stop_animation(): 
        global ANIM
        
        ANIM = False

    # Function to run the model with the user's prompt
    def colleria_ai(prompt):
        response_box.grid_forget()
        button_frame.grid_forget()

        start_animation()

        loading_label.configure(text = "Let me think for a moment")
        loading_label.grid(row = 0, column = 0, padx = 0, pady = (0, 320), sticky = "nsew")
        
        if prompt_var.get() != "Ask Colleria.AI": 
            prompt_entry.delete(0, tk.END)
            frame.focus()
            prompt_entry.configure(text_color = main.TEXT_COLOR)
            prompt_var.set("Ask Colleria.AI") 

            response = colleriaai.colleriaai(str(prompt))

            response_box.configure(state = "normal")

            if response_box.get("1.0", tk.END) != "":
                response_box.delete("1.0", tk.END)

            response_box.insert(tk.END, response)
            response_box.configure(state = "disabled")

            stop_animation()

            loading_label.grid_forget()
            response_box.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
            button_frame.grid(row = 3, column = 0, padx = 160, pady = (2, 12), sticky = "e")

    # Function to run the colleria ai function
    def run_prompt(event = None):
        def check_internet_connection(url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'colleria_ai' function.
            If the connection fails, it will show a popup message to check the internet connection.
            
            :param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds
                prompt = prompt_entry.get()

                if PROMPT == prompt:
                    return
                elif prompt == "" or prompt == "Ask Colleria.AI":
                    popup.open_popup("Please fill in the prompt field", True)
                
                    return
                elif response.status_code == 200 and not (prompt == "" or prompt == "Ask Colleria.AI"):
                    # If the connection is successful, start a thread to run the 'colleria_ai' function
                    thread = threading.Thread(target = colleria_ai, args = (prompt,))

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        check_internet_connection()

    # Function to get the value from the response box and copy it to the clipboard
    def get_value():
        """
        Gets the transcription result from the result box and copies it to the clipboard.
        If the result box is empty, it displays an error message.
        """

        value = response_box.get("1.0", "end-1c")

        if value == "":
            popup.open_popup("No transcription available", True)
        else:
            root.clipboard_clear()
            root.clipboard_append(value)

            popup.open_popup("Copied to clipboard", True)

    # Entry to display the response
    prompt_entry = ctk.CTkEntry(prompt_frame, textvariable = prompt_var, height = 32, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                                corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_TEXT_COLOR, border_width = 2)
    prompt_entry.grid(row = 0, column = 0, padx = 0, pady = 12, sticky = "nsew")
    prompt_entry.bind("<FocusIn>", on_entry_click) 
    prompt_entry.bind("<FocusOut>", on_focus_out)
    prompt_entry.bind("<Return>", run_prompt)

    # Create the ask button
    ask_button = ctk.CTkButton(prompt_frame, text = "Ask", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                               hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 86, 
                               command = run_prompt)
    ask_button.grid(row = 0, column = 1, padx = (8, 0), pady = 12, sticky = "nsew")

    # Button to copy the response to the clipboard
    copy_button = ctk.CTkButton(button_frame, text = "Copy", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64,
                                command = get_value)
    copy_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
