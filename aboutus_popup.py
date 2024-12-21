# Importing necessary libraries and modules
import tkinter as tk
import main

"""
This code contains the function 
used to open the about us popup frame
"""

# Function to open the popup
def open_popup():
    """
    This function creates and displays a popup window with a specified message.
    It performs the following steps:
    1. Initializes the popup window.
    2. Configures the popup window's appearance.
    3. Centers the popup window on the screen.
    """

    # Initialize the popup window
    popup = tk.Tk()
    popup.withdraw()  # Hide the popup window until it's fully configured
    popup.configure(bg = main.BASE_COLOR)
    popup.iconbitmap("public/aboutus_popup.ico")
    popup.title("About us")

    # Create and place the labels in the popup window
    text = ["About Colleria", "Colleria is an open source software that aims to be a tool\nthat can make it easier for students to complete their\nassignments.",
            "Our Mission", "Our biggest mission is to make any school or college\nassignment easy to complete in the shortest possible time.",
            "Contact", "Email: minku.developer23@gmail.com"]

    temp_width = []; temp_height = 0

    for row, label in enumerate(text):
        if row % 2 == 0:
            message_label = tk.Label(popup, text = label, font = (main.FONT, 10, "bold"), fg = main.TEXT_COLOR, bg = main.BASE_COLOR, 
                                     justify = "left")
            message_label.grid(row = row, column = 0, padx = (14, 12), pady = (8, 4), sticky = "w")
        else:
            message_label = tk.Label(popup, text = label, font = (main.FONT, 10, "normal"), fg = main.TEXT_COLOR, bg = main.BASE_COLOR, 
                                     justify = "left")
            message_label.grid(row = row, column = 0, padx = (14, 12), pady = (4, 8), sticky = "w")

        # Count the number of lines in the label
        if label.count("\n") == 0: 
            enter = 1
        else:
            enter = label.count("\n")

        # Calculate the size of the popup window
        temp_width.append(message_label.winfo_reqwidth() - 16)
        temp_height = temp_height + (message_label.winfo_reqheight() * enter) + 1

    # Configure the grid layout to expand the message label with available space
    popup.update_idletasks()  # Update the window to reflect the changes

    # Calculate the size and position to center the popup window on the screen
    if message_label.winfo_exists() or popup.winfo_exists():
        max_width = max(temp_width) + 48
        max_height = temp_height + 24
        min_width = 240
        min_height = max_height

        if max_width < min_width:
            # Center the popup window with minimum width
            x_pos = int((popup.winfo_screenwidth() / 2) - (min_width / 2))
            y_pos = int((popup.winfo_screenheight() / 2) - (min_height / 2))
            
            popup.geometry(f"{min_width}x{min_height}+{x_pos}+{y_pos}")
        else:
            # Center the popup window with maximum width
            x_pos = int((popup.winfo_screenwidth() / 2) - (max_width / 2))
            y_pos = int((popup.winfo_screenheight() / 2) - (max_height / 2))

            popup.geometry(f"{max_width}x{max_height}+{x_pos}+{y_pos}")

    # Disable resizing of the popup window
    popup.resizable(False, False)
    
    # Show the configured popup window
    popup.deiconify()

    # Start the main event loop to display the popup window
    popup.mainloop()
