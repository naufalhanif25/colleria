# Importing necessary libraries and modules
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import notepedia_frame as npf
import taskflow_frame as tff
import sketchpad_frame as spf
import doclab_frame as dlf
import transcriberia_frame as tf
import researcheria_frame as rf
import collenguist_frame as clf
import smartlens_frame as slf
import colleriaai_frame as caf
import flassencia_frame as ff
import yt_courier_frame as ytcf
from PIL import Image, ImageOps
import pywinstyles
import os
import aboutus_popup
import cleaner
import webbrowser
import getpath

# Color constants for the application interface
BASE_COLOR = "#FFFFFF"
FRAME_COLOR = "#F0F9FF"
FG_COLOR = "#38BDF8"
FG_HOVER_COLOR = "#0EA5E9"
FADED_BORDER_COLOR = "#7DD3FC"
BORDER_COLOR = "#38BDF8"
FADED_TEXT_COLOR = "#38BDF8"
FADED_LABEL_COLOR = "#0EA5E9"
ENTRY_COLOR = "#E0F2FE"
TEXT_COLOR = "#082F49"
SCROLLBAR_COLOR = "#E0F2FE"
SCROLLBAR_HOVER_COLOR = "#BAE6FD"

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

ctk.FontManager.load_font(getpath.base("public/font/Manrope-Regular.ttf"))
ctk.FontManager.load_font(getpath.base("public/font/Manrope-Bold.ttf"))

FONT = "Manrope"

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
    root.iconbitmap(getpath.base("public/colleria.ico"))
    root.title("Colleria")

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
    toollist_container = ctk.CTkFrame(left_panel_frame, width = 164, height = 640, fg_color = FRAME_COLOR)
    toollist_container.grid(row = 0, column = 0, padx = 0, pady = (0, 8), sticky = "nsew")
    toollist_container.grid_columnconfigure(0, weight = 1)
    toollist_container.grid_rowconfigure(1, weight = 1)

    toollist_frame = ctk.CTkFrame(toollist_container, width = 164, height = 640, fg_color = FRAME_COLOR)
    toollist_frame.grid(row = 1, column = 0, padx = 0, pady = (0, 12), sticky = "nsew")
    toollist_frame.grid_columnconfigure(0, weight = 1)
    toollist_frame.grid_rowconfigure(0, weight = 1)

    toollist_canvas = ctk.CTkCanvas(toollist_frame, width = 164, height = 632, bg = FRAME_COLOR, highlightthickness = 0)
    toollist_canvas.grid(row = 0, column = 0, sticky = "nsew") 
    toollist_canvas.grid_columnconfigure(0, weight = 1)
    toollist_canvas.grid_rowconfigure(0, weight = 1)

    toollist_button_frame = ctk.CTkFrame(toollist_canvas, width = 152, height = 632, fg_color = FRAME_COLOR) 
    toollist_button_frame.grid(row = 0, column = 0, sticky = "nsew") 
    toollist_button_frame.grid_columnconfigure(0, weight = 1)

    scrollbar = ctk.CTkScrollbar(toollist_frame, orientation = "vertical", command = toollist_canvas.yview, width = 12,
                                 button_color = SCROLLBAR_COLOR, button_hover_color = SCROLLBAR_HOVER_COLOR)
    scrollbar.grid(row = 0, column = 1, padx = 4, pady = 0, sticky = "nsew")

    # Configure canvas for scrollbar
    toollist_canvas.configure(yscrollcommand = scrollbar.set)
    toollist_canvas.create_window((0, 0), window = toollist_button_frame, anchor = "nw", tags = "toollist_button_frame")

    # Update scroll region and width when the frame size changes 
    def on_configure(event): 
        toollist_canvas.configure(scrollregion = toollist_canvas.bbox("all")) 
        toollist_canvas.itemconfig("toollist_button_frame", width = toollist_canvas.winfo_width())
        
    # Bind <Configure> event to on_configure function 
    toollist_canvas.bind("<Configure>", on_configure)

    # Create a frame to hold the other buttons
    other_frame = ctk.CTkFrame(left_panel_frame, width = 164, height = 120, fg_color = FRAME_COLOR)
    other_frame.grid(row = 1, column = 0, padx = 0, pady = (8, 0), sticky = "nsew")
    other_frame.grid_columnconfigure(0, weight = 1)

    # Create a frame for the tool content on the right side
    tool_frame = ctk.CTkFrame(root, width = 760, height = 640, fg_color = FRAME_COLOR)
    tool_frame.grid(row = 0, column = 1, padx = (8, 16), pady = 16, sticky = "nsew")
    tool_frame.grid_columnconfigure(0, weight = 1)

    # Add a welcome label 
    welcome_label = ctk.CTkLabel(tool_frame, text = "Welcome to Colleria", font = (FONT, 36, "bold"), text_color = FADED_TEXT_COLOR)
    welcome_label.grid(row = 0, column = 0, padx = 24, pady = (86, 0), sticky = "nsew")

    # Add a version label
    version_label = ctk.CTkLabel(tool_frame, text = "Version 1.0.0 Beta", font = (FONT, 10, "normal"), text_color = TEXT_COLOR)
    version_label.grid(row = 1, column = 0, padx = 24, pady = (0, 0), sticky = "nsew")

    # Load the image using PIL and convert it to CTkImage
    image = Image.open(getpath.base("public/colleria.png"))
    image = ctk.CTkImage(light_image = image, size = (140, 140))
    
    # Add an icon label with the loaded image
    icon = ctk.CTkLabel(tool_frame, text = "", image = image)
    icon.grid(row = 2, column = 0, padx = 24, pady = (32, 0), sticky = "nsew")

    # Define the message to be displayed in the message label
    message = ("Colleria provides various tools that will support\n"
               "student productivity to complete their assignments\n"
               "effectively and efficiently")

    # Add a message label 
    message_label = ctk.CTkLabel(tool_frame, text = message, font = (FONT, 14, "normal"), text_color = TEXT_COLOR)
    message_label.grid(row = 3, column = 0, padx = 24, pady = (36, 0), sticky = "nsew")
    
    # Add a support label 
    support_label = ctk.CTkLabel(tool_frame, text = " Don't forget to support us by donating ", font = (FONT, 12, "normal"), text_color = TEXT_COLOR)
    support_label.grid(row = 4, column = 0, padx = 24, pady = (16, 0), sticky = "nsew")
    
    pywinstyles.set_opacity(support_label, value = 0.75)  # Set the opacity of the support label
    
    # Load the logo using PIL and convert it to CTkImage
    logo = Image.open(getpath.base("public/minku.png"))
    logo = ctk.CTkImage(light_image = logo, size = (28, 28))

    # Add a logo label
    logo_label = ctk.CTkLabel(tool_frame, text = "", image = logo)
    logo_label.grid(row = 5, column = 0, padx = 24, pady = (0, 16), sticky = "s")
    
    pywinstyles.set_opacity(logo_label, value = 0.25)  # Set the opacity of the logo label
    
    tool_frame.grid_rowconfigure(5, weight = 1)

    # Label for the tool list
    menu_label = ctk.CTkLabel(toollist_container, text = "Tool List", font = (FONT, 16, "bold"), anchor = "w", text_color = TEXT_COLOR)
    menu_label.grid(row = 0, column = 0, padx = 12, pady = 6, sticky = "nsew")

    # Function to change the color of the pressed button
    def change_button_color(button):
        global LAST_PRESSED

        # If there is a previously pressed button, reset its color
        if LAST_PRESSED is not None:
            LAST_PRESSED.configure(fg_color = FG_COLOR, hover_color = FG_HOVER_COLOR, text_color = BASE_COLOR,
                                   border_width = 0, border_color = FRAME_COLOR)

        # Change the color of the currently pressed button
        button.configure(fg_color = BASE_COLOR, hover_color = ENTRY_COLOR, text_color = FADED_TEXT_COLOR, 
                         border_width = 2, border_color = BORDER_COLOR)
        
        # Update the last pressed button to the current button
        LAST_PRESSED = button

    # Create the toollist buttons and commands
    buttons = ["Notepedia", "TaskFlow", "SketchPad", "DocLab", "Transcriberia", "Researcheria", "Collenguist", 
               "SmartLens", "Colleria.AI", "Flassencia", "YT Courier"]
    commands = [lambda: npf.notepedia_tool(root, tool_frame),
                lambda: tff.taskflow_tool(root, tool_frame),
                lambda: spf.sketchpad_tool(root, tool_frame),
                lambda: dlf.doclab_tool(root, tool_frame),
                lambda: tf.transcriber_tool(root, tool_frame), 
                lambda: rf.researcheria_tool(root, tool_frame),
                lambda: clf.collenguist_tool(root, tool_frame),
                lambda: slf.smartlens_tool(root, tool_frame),
                lambda: caf.colleriaai_tool(root, tool_frame),
                lambda: ff.flassencia_tool(root, tool_frame),
                lambda: ytcf.yt_courier_tool(root, tool_frame)]

    for row, (button_text, command) in enumerate(zip(buttons, commands)):
        button = ctk.CTkButton(toollist_button_frame, text = button_text, font = (FONT, 12, "bold"), fg_color = FG_COLOR,
                               hover_color = FG_HOVER_COLOR, text_color = BASE_COLOR, height = 32, width = 152,
                               command = command)
        button.grid(row = row + 1, column = 0, padx = (12, 0), pady = 4, sticky = "nsew")
        button.bind("<Button-1>", lambda event, button = button: change_button_color(button))

    # Create the other buttons
    other_buttons = ["Donate", "About us"]
    commands = [lambda: webbrowser.open_new_tab("https://linktr.ee/minkudev"),
                aboutus_popup.open_popup]
    
    for row, (button_text, command) in enumerate(zip(other_buttons, commands)):
        if row == 0:
            pady = (16, 4)
        elif row == (len(other_buttons) - 1):
            pady = (4, 16)
        else:
            pady = 4

        button = ctk.CTkButton(other_frame, text = button_text, font = (FONT, 12, "bold"), fg_color = FG_COLOR, 
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
