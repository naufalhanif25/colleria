# Importing necessary libraries and modules
import tkinter as tk
import main

"""
This code contains the function 
used to open the popup frame
"""

# Function to open the popup
def open_popup(message, sleep = False):
    """
    This function creates and displays a popup window with a specified message.
    It performs the following steps:
    1. Initializes the popup window.
    2. Configures the popup window's appearance.
    3. Centers the popup window on the screen.
    4. Optionally sets a timer to automatically close the popup after a few seconds.
    
    Parameters:
    - message: The message to be displayed in the popup window.
    - sleep: If True, the popup will automatically close after 2 seconds. Default is False.
    """

    # Initialize the popup window
    popup = tk.Tk()
    popup.withdraw()  # Hide the popup window until it's fully configured
    popup.configure(bg = main.BASE_COLOR)
    popup.iconbitmap("public/message_log.ico")
    popup.title("Message Log")

    # Create and place the message label in the popup window
    message_label = tk.Label(popup, text = message, font = (main.FONT, 10, "normal"), fg = main.TEXT_COLOR, bg = main.BASE_COLOR)
    message_label.grid(row = 0, column = 0, padx = 12, pady = 12, sticky = "nsew")

    # Configure the grid layout to expand the message label with available space
    popup.grid_rowconfigure(0, weight = 1)
    popup.grid_columnconfigure(0, weight = 1)
    popup.update_idletasks()  # Update the window to reflect the changes

    # Calculate the size and position to center the popup window on the screen
    if message_label.winfo_exists() or popup.winfo_exists():
        max_width = message_label.winfo_reqwidth() + 48
        max_height = message_label.winfo_reqheight() + 24
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

    if sleep:
        # If sleep is True, automatically close the popup after 2 seconds
        popup.protocol("WM_DELETE_WINDOW", True)
        popup.after(2000, popup.destroy)

    # Start the main event loop to display the popup window
    popup.mainloop()
