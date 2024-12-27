# Importing necessary libraries
import customtkinter as ctk
import tkinter as tk
import getpath

# Global variable to store the initial state of widget identifiers in the frame
WIDGETS = []

# Function to check if the widget configuration within a frame has changed
def is_exist(frame):
    """
    Function to check if the widget configuration within 
    a frame has changed.
    
    Parameters:
    - frame: The frame to check.
    
    Returns:
    - True if the widget configuration has changed, False otherwise.
    """
    
    global WIDGETS

    # If WIDGETS is empty, initialize it with the current children of the frame
    if not WIDGETS:
        # Get the current children of the frame
        children = frame.winfo_children()
        WIDGETS = children
    else:
        try:
            # Get the current children of the frame
            children = frame.winfo_children()

            # Check if the current children are the same as the initial state
            if children == WIDGETS:
                return False  # Return False if the widgets have not changed
            else:
                # Update the global variable with the new state
                WIDGETS = children

            return True  # Return True if the widgets have changed
        except tk.TclError:
            # Update the global variable with the current state
            WIDGETS = children

            return True  # Return True if there was an error (indicating a change)
