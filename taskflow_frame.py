# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import threading
import main
import popup
import cleaner

# Global variable to hold the current task line value
ROW = 0

# Function to open the TaskFlow frame
def taskflow_tool(root, frame):
   """
   This function initializes the taskflow tool interface 
   within the given root window. It performs the following steps: 
   1. Cleans specific files by calling the clean_file function from the cleaner module. 
   2. Destroys the existing tool_frame. 
   3. Creates a new custom tkinter frame with specified dimensions and color, 
      and places it within the root window. 

   Parameters:
   - root: The root window for the tkinter application
   - frame: The current tool_frame to be replaced with the taskflow tool interface
   """

   global ROW

   ROW = 0  # Resets the row variable value

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

   # Add a label for the taskflow tool frame
   taskflow_label = ctk.CTkLabel(frame, text = "TaskFlow", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
   taskflow_label.grid(row = 0, column = 0, padx = 24, pady = (24, 16), sticky = "nsew")

   # Create a frame for the add task entry
   addtask_frame = ctk.CTkFrame(frame, width = 240, height = 16, fg_color = main.FRAME_COLOR)
   addtask_frame.grid(row = 1, column = 0, padx = 160, pady = (8, 24), sticky = "nsew")
   addtask_frame.grid_columnconfigure(0, weight = 1)
   addtask_frame.grid_rowconfigure(0, weight = 1)

   # Create a text variable for the search entry and set a placeholder text
   addtask_var = tk.StringVar()
   addtask_var.set("Add Task")

   # Function to handle entry click (focus in)
   def on_entry_click(event):
      if addtask_var.get() == "Add Task":
         addtask_entry.configure(text_color = main.TEXT_COLOR)
         addtask_var.set("")

   # Function to handle entry focus out
   def on_focus_out(event):
      if addtask_var.get() == "":
         addtask_entry.configure(text_color = main.FADED_LABEL_COLOR)
         addtask_var.set("Add Task")

   # Create the add task entry widget
   addtask_entry = ctk.CTkEntry(addtask_frame, textvariable = addtask_var, width = 220, height = 16, font = (main.FONT, 12, "normal"),
                                fg_color = main.BASE_COLOR, corner_radius = 16, border_color = main.FADED_BORDER_COLOR)
   addtask_entry.grid(row = 0, column = 0, padx = 0, pady = 4, sticky = "nsew")
   addtask_entry.configure(text_color = main.FADED_LABEL_COLOR)
   addtask_entry.bind("<FocusIn>", on_entry_click)
   addtask_entry.bind("<FocusOut>", on_focus_out)

   # Create a frame for the task buttons frame
   task_frame = ctk.CTkFrame(frame, height = 32, fg_color = main.FRAME_COLOR)
   task_frame.grid(row = 2, column = 0, padx = 120, pady = (0, 24), sticky = "nsew")
   task_frame.grid_columnconfigure(0, weight = 1)
   task_frame.grid_rowconfigure(0, weight = 1)

   frame.grid_rowconfigure(2, weight = 1)

   # Create a frame for the tool list on the left panel frame
   task_panel_frame = ctk.CTkFrame(task_frame, fg_color = main.FRAME_COLOR)
   task_panel_frame.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
   task_panel_frame.grid_columnconfigure(0, weight = 1)
   task_panel_frame.grid_rowconfigure(0, weight = 1)

   task_panel_canvas = ctk.CTkCanvas(task_panel_frame)
   task_panel_canvas.grid(row = 0, column = 0, sticky = "nsew")
   task_panel_canvas.grid_columnconfigure(0, weight = 1)
   task_panel_canvas.grid_rowconfigure(0, weight = 1)

   task_buttons_frame = ctk.CTkFrame(task_panel_canvas, fg_color = main.FRAME_COLOR)
   task_buttons_frame.grid_columnconfigure(0, weight = 1)

   scrollbar = ctk.CTkScrollbar(task_panel_frame, orientation = "vertical", command = task_panel_canvas.yview, width = 12,
                                button_color = main.SCROLLBAR_COLOR, button_hover_color = main.SCROLLBAR_HOVER_COLOR)
   scrollbar.grid(row = 0, column = 1, padx = 4, pady = 0, sticky = "nsew")

   # Configure canvas for scrollbar
   task_panel_canvas.configure(yscrollcommand = scrollbar.set)
   task_panel_canvas.create_window((0, 0), window = task_buttons_frame, anchor = "nw")

   # Update scroll region when the frame size changes
   task_buttons_frame.bind("<Configure>", lambda event: task_panel_canvas.configure(scrollregion = task_buttons_frame.bbox("all")))

   # Function to mark tasks as done
   def task_done(button):
      # Get the row information from the button
      row = button.grid_info()["row"]

      # Open the task log file in binary read mode
      with open("bin/log/task_log.bin", "rb") as file:
         lines = file.read().decode("utf-8").split("\n")  # Read and decode the file contents into a list of lines

      # Remove the line with the specific row
      for index, line in enumerate(lines):
         if str(row) in line:
            lines.pop(index)

      # Write the updated lines back to the file
      with open("bin/log/task_log.bin", "wb") as file:
         file.write("\n".join(lines).encode("utf-8"))

      # Update the button's appearance to indicate the task is done
      button.configure(fg_color = main.FG_COLOR, text = "Task done", text_color = main.BASE_COLOR, hover_color = main.FG_HOVER_COLOR,
                       border_width = 0)

      # Schedule the button to be destroyed after 2 seconds
      root.after(2000, button.destroy)

   # Function to add a new task
   def add_task(event = None, text = None):
      global ROW

      # Get the task text from the entry if not provided
      if text is None:
         text = addtask_entry.get()

      # Check if the task text is valid
      if text != "" and text != "Add Task":
         if not text:
            return

         # Reset the entry and focus back to the root
         addtask_entry.configure(text_color = main.FADED_LABEL_COLOR)
         addtask_var.set("Add Task")
         root.focus_set()

         # Append the new task to the task log file
         with open("bin/log/task_log.bin", "ab") as file:
            file.write(f"{ROW}; {text}\n".encode("utf-8"))

         # Create a button for the new task
         button = ctk.CTkButton(task_buttons_frame, text = text, font = (main.FONT, 12, "normal"), anchor = "center",
                                border_color = main.FADED_TEXT_COLOR, text_color = main.TEXT_COLOR, fg_color = main.FRAME_COLOR,
                                border_width = 1, hover_color = main.ENTRY_COLOR, border_spacing = 8,
                                command = lambda: task_done(button))
         button.grid(row = ROW, column = 0, padx = 0, pady = 4, sticky = "nsew")

         # Ensure the task buttons frame layout is configured
         task_buttons_frame.grid(row = 0, column = 0, sticky = "nsew")
         task_buttons_frame.grid_columnconfigure(0, weight = 1)

         ROW += 1
      else:
         popup.open_popup("Please fill in the add task field", True)  # Show a popup if the task field is empty

   # Function to load tasks from the task log file
   def load_tasks():
      global ROW

      try:
         # Open the task log file in binary read mode
         with open("bin/log/task_log.bin", "rb") as file:
            lines = file.read().decode("utf-8").split("\n")  # Read and decode the file contents into a list of lines

         # Clear the contents of the task log file
         with open("bin/log/task_log.bin", "wb") as file:
            pass

         # Add each task to the GUI
         for line in lines:
            if line.strip():  # Check if the line is not empty
               index, tasks = line.split("; ", 1)
               ROW = int(index)

               add_task(text = tasks.strip())  # Add task to the GUI

               ROW += 1
      except FileNotFoundError as e:
         # Log an error if the task log file is not found
         with open("bin/log/error_log.bin", "wb") as file:
            text = "Task log file not found. Starting with an empty task list"

            file.write(text.encode("utf-8"))
            file.close()

   # Load tasks from file when the program starts
   load_tasks()

   # Create the add task button
   addtask_button = ctk.CTkButton(addtask_frame, text = "Add", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR,
                                  hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 72, corner_radius = 16,
                                  command = lambda: add_task(addtask_entry.get()))
   addtask_button.grid(row = 0, column = 1, padx = (8, 0), pady = 4, sticky = "nsew")

   # Bind the Return key to start the add task
   addtask_entry.bind("<Return>", lambda event: add_task(addtask_entry.get()))
   