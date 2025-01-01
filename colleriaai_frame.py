# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
from tkhtmlview import HTMLLabel
import pywinstyles
import webbrowser
import markdown2
import main
import cleaner
import colleriaai
import threading
import popup
import requests
import getpath
import is_widget

PROMPT = None  # To store the current prompt
ANIM = False  # To control loading animation state
KEY = None  # To store the api key
RESPONSE = ""  # To store the response

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

    global PROMPT, ANIM, KEY, RESPONSE

    # Resets variable values
    PROMPT = None
    ANIM = False
    KEY = None
    RESPONSE = ""

    key_path = getpath.base("model/key.bin")

    # Open the file in read-binary mode
    with open(key_path, "rb") as file:
        KEY = file.read()  # Read the API key from the file
        KEY = KEY.decode("utf-8")

    # Function to display the page when the API key is available
    def key_entered(root, frame):
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

        # Add a label for the model name
        model_label = ctk.CTkLabel(frame, text = f"with {colleriaai.MODEL_NAME}", font = (main.FONT, 12, "normal"), text_color = main.TEXT_COLOR)
        model_label.grid(row = 1, column = 0, padx = 24, pady = (0, 8), sticky = "nsew")

        # Create a frame as a container
        response_container = ctk.CTkFrame(frame, fg_color = main.BASE_COLOR, corner_radius = 16, border_width = 2, border_color = main.FADED_BORDER_COLOR)
        response_container.grid(row = 2, column = 0, padx = 120, pady = 0, sticky = "nsew")
        response_container.grid_columnconfigure(0, weight = 1)
        response_container.grid_rowconfigure(0, weight = 1)

        # Create a frame for the response label
        response_frame = ctk.CTkScrollableFrame(response_container, fg_color = main.BASE_COLOR, scrollbar_fg_color = "transparent",  corner_radius = 16,
                                                scrollbar_button_color = main.SCROLLBAR_COLOR, scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR)
        response_frame.grid(row = 0, column = 0, padx = 6, pady = (6, 0), sticky = "nsew")
        response_frame.grid_columnconfigure(0, weight = 1)
        response_frame.grid_rowconfigure(0, weight = 1)
        
        frame.grid_rowconfigure(2, weight = 1)  # Ensure frame rows expand properly

        # Create a frame for the prompt entry and button
        prompt_frame = ctk.CTkFrame(frame, height = 64, fg_color = main.FRAME_COLOR)
        prompt_frame.grid(row = 3, column = 0, padx = 160, pady = (0, 24), sticky = "nsew")
        prompt_frame.grid_columnconfigure(0, weight = 1)
        prompt_frame.grid_rowconfigure(0, weight = 1)

        # Create a text variable for the prompt entry and set a placeholder text
        prompt_var = tk.StringVar() 
        prompt_var.set("Ask Colleria.AI")
        
        # Create and configure the response label
        response_label = HTMLLabel(response_frame, html = None)
        response_label.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
        response_label.configure(background = main.BASE_COLOR)
        
        # Initially hide the response frame
        response_frame.grid_forget()

        # Create a loading label to show the loading animation
        loading_label = ctk.CTkLabel(response_container, text = "Let me think for a moment", font = (main.FONT, 12, "normal"), 
                                     text_color = main.FADED_LABEL_COLOR, corner_radius = 16)
        loading_label.grid(row = 0, column = 0, padx = 6, pady = (6, 320), sticky = "nsew")
        loading_label.grid_forget()  # Hide the label initially

        # Create a button frame to hold the copy button
        button_frame = ctk.CTkFrame(response_container, height = 24, fg_color = main.BASE_COLOR)
        button_frame.grid(row = 1, column = 0, padx = 12, pady = (0, 12), sticky = "e")
        button_frame.grid_forget()
        button_frame.grid_columnconfigure(0, weight = 1)
        button_frame.grid_rowconfigure(0, weight = 1)

        # Ensure the response container expands properly
        response_container.grid(row = 2, column = 0, padx = 120, pady = (6, 8), sticky = "nsew")
        response_container.grid_rowconfigure(0, weight = 1)
        response_container.grid_columnconfigure(0, weight = 1)

        # Ensure the main frame column expands properly
        frame.grid_columnconfigure(0, weight = 1)

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
            global RESPONSE

            # Hide the response frame and button frame initially
            response_frame.grid_forget()
            button_frame.grid_forget()

            root.configure(cursor = "watch")  # Change the shape of the cursor

            start_animation()  # Start the loading animation

            # Configure and display the loading label
            loading_label.configure(text = "Let me think for a moment")
            loading_label.grid(row = 0, column = 0, padx = 6, pady = (6, 320), sticky = "nsew")
            
            # Check if the prompt is not the default placeholder text
            if prompt_var.get() != "Ask Colleria.AI": 
                prompt_entry.delete(0, tk.END)  # Clear the prompt entry field and reset focus
                frame.focus()
                prompt_entry.configure(text_color = main.TEXT_COLOR)  # Set the text color for the prompt entry
                prompt_var.set("Ask Colleria.AI")  # Reset the prompt variable to default placeholder text

                # Run the Colleria.AI model with the provided prompt
                response = colleriaai.colleriaai(frame, str(prompt))
                
                # Convert the model's response from markdown to HTM
                content = markdown2.markdown(response)
                
                # Store the response globally
                RESPONSE = response
                
                # Apply custom styles to various HTML tags in the content
                content = content.replace("<a>", f"<a style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<b>", f"<b style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<code>", f"<code style=\"font-size: 10px; color: {main.TEXT_COLOR};\">")
                content = content.replace("<em>", f"<em style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h1>", f"<h1 style=\"font-size: 18px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h2>", f"<h2 style=\"font-size: 16px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h3>", f"<h3 style=\"font-size: 14px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h4>", f"<h4 style=\"font-size: 12px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h5>", f"<h5 style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<h6>", f"<h6 style=\"font-size: 8px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<i>", f"<i style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<li>", f"<li style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<mark>", f"<mark style=\"font-size: 10px; color: {main.TEXT_COLOR};\">")
                content = content.replace("<ol>", f"<ol style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<p>", f"<p style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<pre>", f"<pre style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<strong>", f"<strong style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<u>", f"<u style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                content = content.replace("<ul>", f"<ul style=\"font-size: 10px; font-family: {main.FONT}; color: {main.TEXT_COLOR};\">")
                
                # Set the HTML content for the response label and adjust its height
                response_label.set_html(content)
                response_label.fit_height()

                stop_animation()  # Stop the loading animation
                
                root.configure(cursor = "arrow")  # Resets the cursor shape
                
                # Hide the loading label and show the response frame and button frame
                loading_label.grid_forget()
                response_frame.grid(row = 0, column = 0, padx = 6, pady = (6, 0), sticky = "nsew")
                button_frame.grid(row = 1, column = 0, padx = 12, pady = (0, 12), sticky = "e")

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
            Gets the response from the response box and copies it to the clipboard.
            If the response box is empty, it displays an error message.
            """

            # Check if the global RESPONSE variable is empty
            if RESPONSE == "":
                # If empty, open a popup to indicate no response is available
                popup.open_popup("No response available", True)
            else:
                root.clipboard_clear()  # Clear the current clipboard content
                root.clipboard_append(RESPONSE)  # Append the RESPONSE to the clipboard

                # Open a popup to indicate the response has been copied to the clipboard
                popup.open_popup("Copied to clipboard", True)

        # Entry to display the prompt
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
        copy_button = ctk.CTkButton(button_frame, text = "Copy", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, height = 24,
                                    hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, corner_radius = 32,
                                    command = get_value)
        copy_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")

        # Get the current children of the frame
        is_widget.WIDGETS = frame.winfo_children()

    # Function to display the page when the API key is not yet available
    def enter_key(root, frame):
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

        # Add a label for the colleria ai tool frame
        getstarted_label = ctk.CTkLabel(frame, text = "Enter your API key to get started \u2728", font = (main.FONT, 18, "bold"), 
                                        text_color = main.FADED_TEXT_COLOR)
        getstarted_label.grid(row = 1, column = 0, padx = 24, pady = (132, 0), sticky = "nsew")

        # Create a frame for the key entry and button
        key_frame = ctk.CTkFrame(frame, height = 48, fg_color = main.FRAME_COLOR)
        key_frame.grid(row = 2, column = 0, padx = 160, pady = (32, 0), sticky = "nsew")
        key_frame.grid_columnconfigure(0, weight = 1)
        key_frame.grid_rowconfigure(0, weight = 1)

        # Create a text variable for the key entry and set a placeholder text
        key_var = tk.StringVar() 
        key_var.set("Enter the API key")

        # Function to open the Groq console URL in a new browser tab
        def open_groq():
            webbrowser.open_new_tab("https://console.groq.com")

        # Create a frame for the URL button
        url_frame = ctk.CTkFrame(frame, height = 24, fg_color = main.FRAME_COLOR)
        url_frame.grid(row = 3, column = 0, padx = 0, pady = 2, sticky = "n")
        url_frame.grid_columnconfigure(0, weight = 1)

        # Add a label for the URL
        url_label = ctk.CTkLabel(url_frame, text = "Don't have an API key yet?", font = (main.FONT, 10, "normal"), text_color = main.TEXT_COLOR)
        url_label.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "w")

        # Define function to change button text color on hover enter
        def on_enter(event, button):
            button.configure(text_color = main.FG_HOVER_COLOR)

        # Define function to change button text color back on hover leave
        def on_leave(event, button):
            button.configure(text_color = main.FG_COLOR)

        # Create a clickable URL button
        url_button = ctk.CTkButton(url_frame, text = "Get it here", font = (main.FONT, 10, "bold"), fg_color = main.FRAME_COLOR, width = 28,
                                   hover_color = main.FRAME_COLOR, text_color = main.FG_COLOR, command = open_groq)
        url_button.grid(row = 0, column = 1, padx = 0, pady = (2, 0), sticky = "w")

        # Bind hover enter and leave events to the URL button
        url_button.bind("<Enter>", lambda event: on_enter(event, url_button))
        url_button.bind("<Leave>", lambda event: on_leave(event, url_button))

        pywinstyles.set_opacity(url_button, color = main.FRAME_COLOR)  # Set the opacity of the URL button foreground

        # Function to handle entry click (focus in)
        def on_entry_click(event): 
            if key_var.get() == "Enter the API key": 
                key_entry.configure(text_color = main.TEXT_COLOR)
                key_var.set("") 

        # Function to handle entry focus out
        def on_focus_out(event): 
            if key_var.get() == "": 
                key_entry.configure(text_color = main.FADED_LABEL_COLOR)
                key_var.set("Enter the API key")

        # Function to handle enter key press or button click
        def enter(event, root, frame):
            api_key = key_var.get()

            if api_key != "" and api_key != "Enter the API key":
                if api_key.startswith("gsk_"):
                    with open(key_path, "wb") as file:
                        KEY = api_key

                        file.write(KEY.encode("utf-8"))

                    key_entered(root, frame)
                else:
                    popup.open_popup("Invalid API key, please try again", True)
            else:
                popup.open_popup("Please fill in the API key field", True)

        # Entry widget to enter the API key
        key_entry = ctk.CTkEntry(key_frame, textvariable = key_var, height = 32, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                                 corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_TEXT_COLOR, border_width = 2)
        key_entry.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
        key_entry.bind("<FocusIn>", on_entry_click) 
        key_entry.bind("<FocusOut>", on_focus_out)
        key_entry.bind("<Return>", lambda event = None: enter(event, root, frame))

        # Create the enter button
        enter_button = ctk.CTkButton(key_frame, text = "Enter", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 16,
                                     hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 72, 
                                     command = lambda event = None: enter(event, root, frame))
        enter_button.grid(row = 0, column = 1, padx = (8, 0), pady = 0, sticky = "nsew")
        
        # Get the current children of the frame
        is_widget.WIDGETS = frame.winfo_children()

    # Check if the API key is already available
    if KEY != "":
        key_entered(root, frame)
    else:
        enter_key(root, frame)
