# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import webbrowser
import player
import main
import popup as pop
import getpath

"""
This code contains the function 
used to open the researcheria popup frame
"""

# Function to open the popup
def open_popup(detail):
    """
    This function creates and displays a popup window with a specified message.
    It performs the following steps:
    1. Initializes the popup window.
    2. Configures the popup window's appearance.
    3. Centers the popup window on the screen.
    
    Parameters:
    - detail: The details to be displayed in the popup window.
    """

    # Initialize the popup window
    popup = tk.Tk()
    popup.withdraw()  # Hide the popup window until it's fully configured
    popup.configure(bg = main.BASE_COLOR)
    popup.iconbitmap(getpath.base("public/researcheria_popup.ico"))
    popup.title("Detail")

    labels = ["Title", "DOI", "Pub. Date", "Authors", "Citation", "Ranking", "Source"]

    # Create and place the message label in the popup window
    for row, label in enumerate(labels):
        if row == 0:
            pady = (24, 4)
        elif row == len(labels) - 1:
            pady = (4, 12)
        else:
            pady = 4
            
        text_label = tk.Label(popup, text = label, font = (main.FONT, 10, "normal"), anchor = "center", 
                              fg = main.TEXT_COLOR, bg = main.BASE_COLOR)
        text_label.grid(row = row, column = 0, padx = (24, 8), pady = pady, sticky = "w")

        text_box = ctk.CTkTextbox(popup, fg_color = main.BASE_COLOR, font = (main.FONT, 12, "normal"), border_color = main.FADED_LABEL_COLOR, 
                                  border_width = 1, text_color = main.TEXT_COLOR, scrollbar_button_color = main.SCROLLBAR_COLOR,
                                  scrollbar_button_hover_color = main.SCROLLBAR_HOVER_COLOR, width = 320, height = 32)
        text_box.grid(row = row, column = 1, padx = (8, 24), pady = pady, sticky = "e")
        text_box.configure(state = "normal")  # Enable editing to insert text

        text_box.insert("1.0", detail[row])

        text_box.configure(state = "disabled")  # Disable editing after insertion

    # Function to get the value from the result box and copy it to the clipboard
    def get_value():
        """
        Gets the transcription result from the result box and copies it to the clipboard.
        If the result box is empty, it displays an error message.
        """

        value = detail[4]

        popup.clipboard_clear()
        popup.clipboard_append(value)

        pop.open_popup("Copied to clipboard", True)

    # Function to open the url in the default browser
    def browse_url():
        webbrowser.open_new_tab(detail[6])

    def browse_ranking():
        webbrowser.open_new_tab(detail[5])

    # Create and place the buttons in the popup window
    button_frame = ctk.CTkButton(popup, text = "", fg_color = main.BASE_COLOR, hover = False)
    button_frame.grid(row = 7, column = 1, padx = 24, pady = (0, 24), sticky = "e")

    if len(detail[5]) > 2:
        ranking_button = ctk.CTkButton(button_frame, text = "Ranking", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                       hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, width = 64, 
                                       command = browse_ranking)
        ranking_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "e")

    browse_button = ctk.CTkButton(button_frame, text = "Browse", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                  hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, width = 64, 
                                  command = browse_url)
    browse_button.grid(row = 0, column = 1, padx = (8, 0), pady = 0, sticky = "e")

    cite_button = ctk.CTkButton(button_frame, text = "Cite", font = (main.FONT, 12, "bold"), fg_color = main.FG_COLOR,
                                hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, height = 32, width = 64, 
                                command = get_value)
    cite_button.grid(row = 0, column = 2, padx = (8, 0), pady = 0, sticky = "e")

    # Configure the grid layout to expand the message label with available space
    popup.update_idletasks()  # Update the window to reflect the changes

    # Calculate the size and position to center the popup window on the screen
    if popup.winfo_exists(): # Check if the popup window exists
        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()
        x_pos = int((popup.winfo_screenwidth() / 2) - (width / 2))
        y_pos = int((popup.winfo_screenheight() / 2) - (height / 2))

        popup.grid_columnconfigure(1, weight = 1)
        popup.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    # Disable resizing of the popup window
    popup.resizable(False, False)
    
    # Show the configured popup window
    popup.deiconify()

    # Plays log sound effects
    player.playsound(getpath.base("public/sfx/research_sfx.wav"))

    # Start the main event loop to display the popup window
    popup.mainloop()
