# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import requests
from PIL import Image
import segno
import os
import cleaner
import main
import is_widget
import getpath
import popup

# Variable to store the path
PATH = ""

# Function to open the Swift-QR frame
def swiftqr_tool(root, frame):
    """
    This function initializes the swift qr tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the swift qr tool interface
    """
    
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

    # Add a label for the swift qr tool frame
    swiftqr_label = ctk.CTkLabel(frame, text = "Swift-QR", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    swiftqr_label.grid(row = 0, column = 0, padx = 24, pady = (24, 0), sticky = "nsew")
    
    # Create a frame for the url entry and button
    url_frame = ctk.CTkFrame(frame, width = 860, height = 32, fg_color = main.FRAME_COLOR)
    url_frame.grid(row = 1, column = 0, padx = 160, pady = (32, 0), sticky = "nsew")
    url_frame.grid_columnconfigure(0, weight = 1)
    url_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame to display the QR code result
    result_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR, border_width = 2, border_color = main.FADED_BORDER_COLOR, corner_radius = 16)
    result_frame.grid(row = 2, column = 0, padx = 240, pady = (36, 32), sticky = "nsew")
    result_frame.grid_columnconfigure(0, weight = 1)
    result_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame to display the generated QR code
    qrcode_frame = ctk.CTkFrame(result_frame, fg_color = main.FRAME_COLOR, corner_radius = 8)
    qrcode_frame.grid(row = 0, column = 0, padx = 16, pady = (8, 16), sticky = "nsew")
    qrcode_frame.grid_columnconfigure(0, weight = 1)
    qrcode_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame for action buttons (Save and Direct)
    buttons_frame = ctk.CTkFrame(result_frame, fg_color = main.FRAME_COLOR, height = 48, corner_radius = 8)
    buttons_frame.grid(row = 1, column = 0, padx = 16, pady = (0, 8), sticky = "e")
    buttons_frame.grid_columnconfigure(0, weight = 1)
    buttons_frame.grid_rowconfigure(0, weight = 1)
    buttons_frame.grid_forget()
    
    # Function to save the QR code
    def save_qrcode():
        global PATH
        
        # Path to the temporary QR code image
        path = getpath.base("temp/temp.png")
        
        # Open a file dialog to select save location and file format (PNG or JPEG)
        PATH = filedialog.asksaveasfilename(title = "Select a sketch", 
                                            filetypes = [("PNG File", "*.png"),
                                                         ("JPEG File", "*.jpeg")],
                                            defaultextension = (".png", ".jpeg"))
        
        # Open the temporary QR code image
        image = Image.open(path)
        
        image.save(PATH)  # Save the image to the selected path
        
        # Show a popup to confirm the file has been saved
        popup.open_popup(f"File are saved to\n{PATH}", True)
        
        # Remove the temporary image file
        if os.path.exists(path):
            os.remove(path)
    
    # Function to browse the output directory
    def browse_directory():
        if PATH == "":
            # Show a popup if no QR code has been saved
            popup.open_popup("No QR code has been saved", True)
        else:
            # Open the directory containing the saved QR code
            os.startfile(os.path.dirname(PATH))
    
    # Create a Save button with specified text, font, and actions
    save_button = ctk.CTkButton(buttons_frame, text = "Save", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 68, 
                                command = save_qrcode)
    save_button.grid(row = 0, column = 0, padx = (0, 8), pady = 8, sticky = "e")
    
    # Create a Direct button with specified text, font, and actions
    direct_button = ctk.CTkButton(buttons_frame, text = "Direct", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 8,
                                  hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 68, 
                                  command = browse_directory)
    direct_button.grid(row = 0, column = 1, padx = 0, pady = 8, sticky = "e")
    
    frame.grid_rowconfigure(2, weight = 1)

    # Create a text variable for the url entry and set a placeholder text
    url_var = tk.StringVar() 
    url_var.set("Enter the URL")
    
    # Function to handle entry click (focus in)
    def on_entry_click(event): 
        if url_var.get() == "Enter the URL": 
            url_entry.configure(text_color = main.TEXT_COLOR)
            url_var.set("") 

    # Function to handle entry focus out
    def on_focus_out(event): 
        if url_var.get() == "": 
            url_entry.configure(text_color = main.FADED_LABEL_COLOR)
            url_var.set("Enter the URL")
    
    # Function to generate QR code      
    def swiftqr(event = None):
        global PATH
        
        url = url_entry.get()
        
        if url == "Enter the URL" or url == "":
            # Show a popup if the URL field is empty
            popup.open_popup("Please fill in the URL field", True)
        else:
            PATH = ""

            # Path to the temporary QR code image
            path = getpath.base("temp/temp.png")
            qrcode = segno.make_qr(url)  # Generate a QR code from the URL
            
            # Set the cursor to 'watch' while processing
            root.configure(cursor = "watch")
            
            # Save the generated QR code
            qrcode.save(path, scale = 32, border = 2)
            
            # Open the temporary QR code image
            image = Image.open(path)
            image = ctk.CTkImage(light_image = image, size = (320, 320))
            
            # Display the QR code image in the qrcode_frame
            qrcode_preview = ctk.CTkLabel(qrcode_frame, text = "", image = image)
            qrcode_preview.grid(row = 0, column = 0, padx = 24, pady = 24, sticky = "nsew")
            
            # Show the buttons frame
            buttons_frame.grid(row = 1, column = 0, padx = 16, pady = (0, 16), sticky = "nsew")
            
            # Reset the cursor to 'arrow' after processing
            root.configure(cursor = "arrow")
        
    # Function to start the transcription process in a separate thread
    def run_swiftqr():
        """
        Starts the YT Courier process in a separate thread to avoid blocking the GUI.
        """

        def check_internet_connection(url = "http://www.google.com/"):
            """
            This function checks the internet connection by sending an HTTP request to the provided URL.
            If the connection is successful, it will start a thread to run the 'swiftqr' function.
            If the connection fails, it will show a popup message to check the internet connection.

            param url: URL used to check the internet connection. Default is http://www.google.com/
            """

            try:
                response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds

                if response.status_code == 200:
                    # If the connection is successful, start a thread to run the 'swiftqr' function
                    thread = threading.Thread(target = swiftqr)

                    thread.start()
                else:
                    # If the connection fails (status code is not 200), show a popup message
                    popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)
            except requests.ConnectionError:
                # If a connection error occurs, show a popup message
                popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

        # Call the function to check the internet connection
        check_internet_connection()
            
    # Entry to display the url
    url_entry = ctk.CTkEntry(url_frame, textvariable = url_var, width = 860, height = 32, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), 
                             corner_radius = 16, text_color = main.FADED_LABEL_COLOR, border_color = main.FADED_BORDER_COLOR, border_width = 2)
    url_entry.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
    url_entry.bind("<FocusIn>", on_entry_click) 
    url_entry.bind("<FocusOut>", on_focus_out)
    url_entry.bind("<Return>", run_swiftqr)
    
    # Create the generate button
    generate_button = ctk.CTkButton(url_frame, text = "Generate", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR, corner_radius = 32,
                                    hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 100, 
                                    command = run_swiftqr)
    generate_button.grid(row = 0, column = 1, padx = (8, 0), pady = 0, sticky = "nsew")
    