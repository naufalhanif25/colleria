# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImagePath
import pywinstyles
import colorsys
import math
import os
import io
import popup
import main
import cleaner
import is_widget

# Global variables to manage the state of the canvas
TITLE = "Untitled"
PATH = ""
CHANGE = False
LINES = 0
ITEMS = []

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Variable to keep track of the last selected color button
LAST_PICKED = None 

# Variables to store the current line color and line width
COLOR = "#000000"
WIDTH = 2

# Function to open the SketchPad frame
def sketchpad_tool(root, frame):
    """
    This function initializes the sketchpad tool interface 
    within the given root window. It performs the following steps: 
    1. Cleans specific files by calling the clean_file function from the cleaner module. 
    2. Destroys the existing tool_frame. 
    3. Creates a new custom tkinter frame with specified dimensions and color, 
       and places it within the root window. 

    Parameters:
    - root: The root window for the tkinter application
    - frame: The current tool_frame to be replaced with the sketchpad tool interface
    """

    global TITLE, PATH, CHANGE, LINES, ITEMS, LAST_PRESSED, LAST_PICKED, COLOR, WIDTH

    # Resets variable values
    TITLE = "Untitled"
    PATH = ""
    CHANGE = False
    LINES = 0
    ITEMS = []
    LAST_PRESSED = None
    LAST_PICKED = None 
    COLOR = "#000000"
    WIDTH = 2
    
    # Variables to store the previous position
    LAST_X = None
    LAST_Y = None

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

    # Add a label for the sketchpad tool frame
    sketchpad_label = ctk.CTkLabel(frame, text = "SketchPad", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
    sketchpad_label.grid(row = 0, column = 0, padx = 24, pady = (24, 12), sticky = "nsew")

    # Create a frame as a container
    container = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
    container.grid(row = 1, column = 0, padx = 16, pady = (0, 16), sticky = "nsew")
    container.grid_columnconfigure(0, weight = 1)
    container.grid_rowconfigure(2, weight = 1)

    # Create a header frame inside the container
    header_frame = ctk.CTkFrame(container, height = 32, fg_color = main.FRAME_COLOR, corner_radius = 8)
    header_frame.grid(row = 0, column = 0, padx = 8, pady = 0, sticky = "nsew")
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

    # Function to create a new sketch
    def new_sketch():
        """ 
        This function creates a new sketch by resetting
        the title and the content of the canvas. 
        """
        
        global TITLE, CHANGE, LAST_X, LAST_Y, ITEMS, PATH

        if not CHANGE:
            TITLE = "Untitled"  # Change the title to Untitled
            
            filename_label.configure(text = TITLE)  # Reset file name label
            canvas.delete("all")  # Clear the canvas
            
            CHANGE = False  # Resets the change variable to false
        else:
            # Open a popup to remind the user to save their sketch
            popup.open_popup("Please save your sketch first before creating a new sketch", True)
            
        # Resets variable values
        LAST_X = None
        LAST_Y = None
        PATH = ""
        ITEMS = []

    # Function to open existing sketch
    def open_sketch():
        """ 
        This function opens an existing sketch by loading 
        its content from a file selected by the user. 
        """
        
        global TITLE, PATH, CHANGE, LAST_X, LAST_Y, ITEMS

        if not CHANGE:
            # Opening the path with the file manager
            PATH = filedialog.askopenfilename(defaultextension = ".png",
                                              filetypes = [("PNG files", "*.png"), 
                                                           ("JPEG files", ("*.jpg", "*.jpeg")),
                                                           ("All files", "*.*")],
                                              title = "Select a sketch")
            if PATH:
                TITLE = os.path.basename(PATH)
                
                filename_label.configure(text = TITLE)  # Update the filename label
                
                image = tk.PhotoImage(file = PATH)
                
                canvas.create_image(0, 0, anchor = "nw", image = image)  # Display the image on the canvas
                canvas.image = image  # Keep a reference to avoid garbage collection
                
                CHANGE = False
        else:
            # Open a popup to remind the user to save their sketch
            popup.open_popup("Please save your sketch before opening an existing sketch", True)
        
        # Resets variable values
        LAST_X = None
        LAST_Y = None
        ITEMS = []

    # Function to save a sketch
    def save_sketch():
        """ 
        This function saves the current sketch to a file. 
        If the sketch has not been saved before, 
        it prompts the user to select a file path. 
        """
        
        global TITLE, PATH, CHANGE
        
        # Function to save the canvas as an image file
        def save(canvas, path, exist = False): 
            global ITEMS
                    
            canvas.update() 
                    
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if exist:
                bg = Image.open(path).resize((width, height))
                image = bg.copy()  # Copy the background image
                draw = ImageDraw.Draw(image)
            else:
                image = Image.new("RGB", (width, height), "#FFFFFF")  # Create a new blank image
                draw = ImageDraw.Draw(image)
                    
            for item in ITEMS:
                coords, color, width = item
                line_path = ImagePath.Path(coords)  # Convert to ImagePath to make curved joints 
                
                # Draw start and end circles for smooth lines
                if len(coords) > 0:
                    x_start, y_start = coords[0]
                    x_end, y_end = coords[-1]
                    
                    draw.ellipse((x_start - (width / 2), y_start - (width / 2), x_start + (width / 2), y_start + (width / 2)), fill = color,
                                 width = width)
                    draw.ellipse((x_end - (width / 2), y_end - (width / 2), x_end + (width / 2), y_end + (width / 2)), fill = color,
                                 width = width)

                draw.line(line_path, fill = color, width = round(width), joint = "curve")  # Draw the sketch lines on the image
                
            image.save(path)  # Save the image to the specified path

        if PATH and os.path.exists(PATH):
            save(canvas, PATH, True)  # Save the sketch with the existing background
            
            TITLE = os.path.basename(PATH)
                
            filename_label.configure(text = TITLE)  # Update the filename label
            
            CHANGE = False
        else:
            # Opening the path with the file manager
            PATH = filedialog.asksaveasfilename(defaultextension = ".png",
                                                filetypes = [("PNG files", "*.png"), 
                                                             ("JPEG files", ("*.jpg", "*.jpeg")),
                                                             ("All files", "*.*")],
                                                title = "Save sketch")
            if PATH:                    
                save(canvas, PATH)  # Save the sketch to the new path
                
                TITLE = os.path.basename(PATH)

                filename_label.configure(text = TITLE)  # Update the filename label
                
                CHANGE = False
            else:
                return  # Exit if the user cancels the save dialog

    # Define buttons and their corresponding commands
    buttons = ["New", "Open", "Save"]
    commands = [new_sketch, open_sketch, save_sketch]

    # Create buttons and add them to the buttons frame
    for index, (button_name, command) in enumerate(zip(buttons, commands)):
        if index == 0 or index == len(buttons) - 1:
            padx = 0
        else:
            padx = 8

        button = ctk.CTkButton(buttons_frame, text = button_name, font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                               hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, command = command)
        button.grid(row = 0, column = index, padx = padx, pady = 8, sticky = "nsew")
    
    # Create a tools frame inside the container
    tools_frame = ctk.CTkFrame(container, height = 32, fg_color = main.ENTRY_COLOR, corner_radius = 8)
    tools_frame.grid(row = 1, column = 0, padx = 0, pady = (0, 8), sticky = "nsew")
    tools_frame.grid_columnconfigure(0, weight = 1)
    tools_frame.grid_columnconfigure(1, weight = 1)
    tools_frame.grid_columnconfigure(2, weight = 1)
    tools_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a frame for the options inside the tools frame
    options_frame = ctk.CTkFrame(tools_frame, height = 32, fg_color = main.ENTRY_COLOR, corner_radius = 8)
    options_frame.grid(row = 0, column = 0, padx = 12, pady = 0, sticky = "nsew")
    options_frame.grid_rowconfigure(0, weight = 1)
    
    # Function to change the color of the pressed button
    def change_button_color(event, button):
        global LAST_PRESSED

        # If there is a previously pressed button, reset its color
        if LAST_PRESSED is not None:
            LAST_PRESSED.configure(fg_color = main.FG_COLOR, hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, 
                                   border_width = 0, border_color = main.ENTRY_COLOR)

        # Change the color of the currently pressed button
        button.configure(fg_color = main.BASE_COLOR, hover_color = main.ENTRY_COLOR, text_color = main.FADED_TEXT_COLOR,
                         border_width = 1, border_color = main.BORDER_COLOR)
        
        # Update the last pressed button to the current button
        LAST_PRESSED = button
    
    # Define options and their corresponding commands
    options = ["Draw", "Erase", "Clear"]
    commands = [lambda: set_mode("draw"), lambda: set_mode("erase"), lambda: set_mode("clear")]

    # Create option buttons and add them to the options frame
    for index, (button_name, command) in enumerate(zip(options, commands)):
        if index == 0 or index == len(options) - 1:
            padx = 0
        else:
            padx = 8

        button = ctk.CTkButton(options_frame, text = button_name, font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR, corner_radius = 32,
                               hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 64, height = 16, command = command)
        button.grid(row = 0, column = index, padx = padx, pady = 8, sticky = "nsew")
        
        # Bind all buttons except the button named Clear
        if button_name != "Clear":
            button.bind("<Button-1>", lambda event, button = button: change_button_color(event, button))
        
        # Automatically configure the color for the default button
        if index == 0:
            change_button_color(None, button)
            
    # Create a frame for the colors inside the tools frame
    colors_frame = ctk.CTkFrame(tools_frame, height = 32, fg_color = main.ENTRY_COLOR, corner_radius = 8)
    colors_frame.grid(row = 0, column = 1, padx = 12, pady = 0, sticky = "nsew")
    colors_frame.grid_rowconfigure(0, weight = 1)
    
    # Function to change the color of the pressed button
    def color_button_config(event, button):
        global LAST_PICKED

        # If there is a previously pressed button, reset its color
        if LAST_PICKED is not None:
            LAST_PICKED.configure(border_width = 0, border_color = main.ENTRY_COLOR)

        # Change the color of the currently pressed button
        button.configure(border_width = 1, border_color = main.BORDER_COLOR)
        
        # Update the last pressed button to the current button
        LAST_PICKED = button
    
    # Function to open color picker and set the selected color to the button  
    def pick_color(button):
        global COLOR
        
        # Open the color picker dialog
        hex_code = colorchooser.askcolor(title = "Choose a color")
        
        try:
            if hex_code:
                # Set the global COLOR variable to the selected color
                COLOR = hex_code[1]
                hover_color = darken_color(COLOR)
                
                # Configure the button with the selected color and its hover color
                button.configure(fg_color = COLOR, hover_color = hover_color)
        except ValueError:
            return
    
    # Function to change the selected color
    def change_color(color):
        global COLOR
        
        COLOR = color
    
    # Define colors and their corresponding commands
    colors = ["#000000", "#FF0000", "#FFFF00", "#00FF00", "#0000FF", "#808080", main.BASE_COLOR]
    commands = [lambda: change_color("#000000"),
                lambda: change_color("#FF0000"),
                lambda: change_color("#FFFF00"),
                lambda: change_color("#00FF00"),
                lambda: change_color("#0000FF"),
                lambda: change_color("#808080"),
                lambda: pick_color(button)]
    
    # Function to darken the color for hover effect
    def darken_color(color, factor = 0.8):
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        
        h, l, s = colorsys.rgb_to_hls(*[x / 255.0 for x in rgb])
        l = max(0, min(1, l * factor))
        
        darker_rgb = colorsys.hls_to_rgb(h, l, s)
        
        return "#%02x%02x%02x" % (int(darker_rgb[0] * 255), int(darker_rgb[1] * 255), int(darker_rgb[2] * 255))

    # Create color buttons and add them to the options frame
    for index, (command, color) in enumerate(zip(commands, colors)):
        hover_color = darken_color(color)  # Calculate the hover color which is a darker shade of the original color
        
        button = ctk.CTkButton(colors_frame, text = "", fg_color = color, hover_color = hover_color, border_width = 0, border_color = main.BORDER_COLOR, 
                               corner_radius = 4, width = 24, height = 16, command = command)
        button.grid(row = 0, column = index, padx = 4, pady = 12, sticky = "nsew")
        
        # Automatically configure the color for the default button
        if index == 0:
            color_button_config(None, button)
        
        # Configure the last button as a custom color picker
        if index == (len(colors) - 1):
            button.configure(text = "\u2795", font = (main.FONT, 8, "normal"), width = 26, text_color = main.TEXT_COLOR)
            button.grid_configure(pady = 10)
            
        # Bind event to change the color of the button when pressed
        button.bind("<Button-1>", lambda event, button = button: color_button_config(event, button))
    
    # Create a frame for the slider inside the tools frame
    slider_frame = ctk.CTkFrame(tools_frame, height = 32, fg_color = main.ENTRY_COLOR, corner_radius = 8)
    slider_frame.grid(row = 0, column = 2, padx = 0, pady = 0, sticky = "nsew")
    slider_frame.grid_columnconfigure(0, weight = 1)
    slider_frame.grid_rowconfigure(0, weight = 1)
    
    # Create a slider inside the slider frame
    slider = ctk.CTkSlider(slider_frame, from_ = 1, to = 100, fg_color = main.BASE_COLOR, button_color = main.FG_COLOR, height = 16,
                           button_hover_color = main.FG_HOVER_COLOR, progress_color = main.FADED_BORDER_COLOR)
    slider.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")
    slider.set(2)  # Set the default value of the slider

    # Create a canvas for drawing
    canvas = ctk.CTkCanvas(container, bg = "#FFFFFF", cursor = "plus", highlightthickness = 1, highlightbackground = main.BORDER_COLOR)
    canvas.grid(row = 2, column = 0, sticky = "nsew")
    
    # Function to update the filename label
    def update_title(): 
        """ 
        This function will update the title if 
        the canvas has been filled with sketches
        """

        global CHANGE

        # Get the number of lines on the canvas
        lines = len(canvas.find_all())

        if lines != LINES: 
            CHANGE = True  # Update the change variable to false

            # Update the title with an asterisk (*)
            filename_label.configure(text = TITLE + "*") 
        else:
            CHANGE = False  # Resets the change variable to false

            # Update the title without an asterisk (*)
            filename_label.configure(text = TITLE) 
    
    # Function to set the last mouse position
    def set_last_draw(event):
        global LAST_X, LAST_Y
        
        LAST_X = event.x
        LAST_Y = event.y
        
        ITEMS.append(([(LAST_X, LAST_Y)], COLOR, WIDTH))  # Add starting point coordinates with default attributes

    # Function to draw on the canvas
    def draw(event):
        global LAST_X, LAST_Y, ITEMS, WIDTH
        
        WIDTH = round(slider.get())
        
        if LAST_X is not None and LAST_Y is not None:
            line_id = canvas.create_line(LAST_X, LAST_Y, event.x, event.y, width = WIDTH, fill = COLOR, capstyle = ctk.ROUND, smooth = ctk.TRUE)
            
            ITEMS[-1][0].append((event.x, event.y))  # Add endpoint coordinates
            ITEMS[-1] = (ITEMS[-1][0], COLOR, WIDTH)  # Update color and width attributes
            
        LAST_X = event.x
        LAST_Y = event.y
        
        update_title()  # Update the title each time a line is erase
    
    # Function to set the last mouse position for the eraser
    def set_last_erase(event):
        global LAST_X, LAST_Y
        
        LAST_X = event.x
        LAST_Y = event.y
    
    # Function to use the eraser on the canvas
    def erase(event):
        global LAST_X, LAST_Y, WIDTH
        
        WIDTH = round(slider.get())
        
        if LAST_X is not None and LAST_Y is not None:
            canvas.create_oval(LAST_X - WIDTH, LAST_Y - WIDTH, LAST_X + WIDTH, LAST_Y + WIDTH, outline = "", fill = "#FFFFFF")
        
        LAST_X = event.x
        LAST_Y = event.y
        
        update_title()  # Update the title each time a line is drawn

    # Function to reset the last mouse position
    def reset(event):
        global LAST_X, LAST_Y
        
        LAST_X = None
        LAST_Y = None
    
    # Function to switch between drawing and erasing modes
    def set_mode(mode):        
        if mode == "draw":  # Drawing mode            
            canvas.bind("<Button-1>", set_last_draw)
            canvas.bind("<B1-Motion>", draw)
            canvas.configure(cursor = "plus")  # Change the shape of the cursor
        elif mode == "erase":  # Erasing mode            
            canvas.bind("<Button-1>", set_last_erase)
            canvas.bind("<B1-Motion>", erase)
            canvas.configure(cursor = "target")  # Change the shape of the cursor
        elif mode == "clear":
            canvas.delete("all")  # Clear the canvas
        
        canvas.bind("<ButtonRelease-1>", reset)
        
        update_title()  # Update the title every time the mode is changed

    # Bind mouse events to the canvas
    canvas.bind("<Button-1>", set_last_draw)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", reset)

    # Get the current children of the frame
    is_widget.WIDGETS = frame.winfo_children()
