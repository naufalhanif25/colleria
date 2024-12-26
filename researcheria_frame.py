# Importing necessary libraries and modules
import customtkinter as ctk
import tkinter as tk
import main
import cleaner
import researcheria
import threading
import webbrowser
import popup
from tkinter.font import Font
import researcheria_popup
import requests
import asyncio
import is_widget

# Variable initialization
RESULTS = None  # To store search results
SEARCH = None  # To store the current search query
DETAIL = {}  # To store detailed information about search results
ANIM = False  # To control loading animation state
PAGE_SIZE = 10 # Number of results per page 
CUR_PAGE = 1 # Current page number

# Variable to keep track of the last pressed button
LAST_PRESSED = None 

# Function to open the Researcheria frame
def researcheria_tool(root, frame):
   """
   Initializes the researcheria tool interface within the given root window. 
   It performs the following steps: 
   1. Cleans specific files by calling the clean_file function from the cleaner module. 
   2. Destroys the existing tool_frame. 
   3. Creates a new custom tkinter frame with specified dimensions and color, 
      and places it within the root window.

   Parameters:
   - root: The root window for the tkinter application
   - frame: The current tool_frame to be replaced with the researcheria tool interface
   """

   global RESULTS, SEARCH, DETAIL, ANIM, CUR_PAGE, LAST_PRESSED

   # Resets the values ​​of variables
   RESULTS = None
   SEARCH = None
   DETAIL = {}
   ANIM = False
   LAST_PRESSED = None 

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

   # Add a label for the researcheria tool frame
   researcheria_label = ctk.CTkLabel(frame, text = "Researcheria", font = (main.FONT, 24, "bold"), text_color = main.TEXT_COLOR)
   researcheria_label.grid(row = 0, column = 0, padx = 24, pady = (24, 16), sticky = "nsew")

   # Create a frame for the search entry
   search_frame = ctk.CTkFrame(frame, width = 240, height = 16, fg_color = main.FRAME_COLOR)
   search_frame.grid(row = 1, column = 0, padx = 160, pady = (8, 24), sticky = "nsew")
   search_frame.grid_columnconfigure(0, weight = 1)
   search_frame.grid_rowconfigure(0, weight = 1)
   search_frame.grid_rowconfigure(2, weight = 1)

   # Create a text variable for the search entry and set a placeholder text
   search_var = tk.StringVar() 
   search_var.set("Search by title")

   # Function to handle entry click (focus in)
   def on_entry_click(event): 
      if search_var.get() == "Search by title": 
         search_entry.configure(text_color = main.TEXT_COLOR)
         search_var.set("") 

   # Function to handle entry focus out
   def on_focus_out(event): 
      if search_var.get() == "": 
         search_entry.configure(text_color = main.FADED_LABEL_COLOR)
         search_var.set("Search by title")
   
   # Create the search entry widget
   search_entry = ctk.CTkEntry(search_frame, textvariable = search_var, width = 220, height = 16, font = (main.FONT, 12, "normal"), 
                               fg_color = main.BASE_COLOR, corner_radius = 16, border_color = main.FADED_BORDER_COLOR)
   search_entry.grid(row = 0, column = 0, padx = 0, pady = 4, sticky = "nsew")
   search_entry.configure(text_color = main.FADED_LABEL_COLOR)
   search_entry.bind("<FocusIn>", on_entry_click) 
   search_entry.bind("<FocusOut>", on_focus_out)

   # Create a loading label to show the loading animation
   loading_label = ctk.CTkLabel(frame, text = "Looking for a match", font = (main.FONT, 12, "normal"), text_color = main.FADED_LABEL_COLOR)
   loading_label.grid(row = 2, column = 0, padx = 0, pady = 0, sticky = "nsew")
   loading_label.grid_forget()  # Hide the label initially

   # Create a button frame to hold the buttons
   button_frame = ctk.CTkFrame(frame, fg_color = main.FRAME_COLOR)
   button_frame.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "nsew")
   button_frame.grid_columnconfigure(0, weight = 1)

   frame.grid_rowconfigure(3, weight = 1)

   # Create a page button frame to hold the page buttons
   page_frame = ctk.CTkFrame(frame,height = 48, fg_color = main.FRAME_COLOR)
   page_frame.grid(row = 4, column = 0, padx = 160, pady = 0, sticky = "nsew")
   page_frame.grid_rowconfigure(0, weight = 1)

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

      animate_loading(loading_label, "Looking for a match")

   # Function to stop the loading animation
   def stop_animation(): 
      global ANIM
      
      ANIM = False

   # Function to display "no results found"
   def no_results_found(label):
      label.configure(text = "No results found")

      root.after(2000, lambda: label.grid_forget())

   # Function to truncate text to fit within a specified width
   def truncate_text(text, max_length, font = Font(family = main.FONT, size = 12, weight = "bold")): 
      width = font.measure(text)

      if width <= max_length: 
         return text

      while width > max_length and len(text) > 0:
         text = text[:-1]
         width = font.measure(text + "...")
      
      return text + "..."

   # Function to wrap text to fit within a specified width
   def wrap_text(text, width):
      words = text.split(" ") 
      lines = [] 
      current_line = "" 
      
      if len(text) <= width:
         return text
      
      for word in words: 
         if len(current_line + " " + word) <= width: 
            current_line += " " + word 
         else: 
            lines.append(current_line.strip()) 
            current_line = word 
      
      lines.append(current_line.strip()) 

      return "\n".join(lines)

   # Function to create buttons for each search result
   def create_buttons(page):
      global DETAIL, PAGE_SIZE

      button_frame.grid_forget() 
      button_frame.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "nsew") 
      
      start_idx = (page - 1) * PAGE_SIZE 
      end_idx = min(start_idx + PAGE_SIZE, len(RESULTS))

      # Remove all existing widgets in button frame
      for widget in button_frame.winfo_children(): 
         widget.destroy() 
         
      # Create a button for each search result on the current page
      for index in range(start_idx, end_idx): 
         result_list = RESULTS[index].split("; ") 

         text = result_list[0] 
         full_text = [result_list[0], result_list[1], result_list[2], result_list[3], 
                      result_list[4], result_list[5], result_list[6]] 
         
         DETAIL[truncate_text(text, 780)] = full_text 
         
         # Function to open the detail popup when button is clicked
         def open_detail(button_text):             
            researcheria_popup.open_popup(DETAIL[button_text])

         # Create a button for each search result
         button = ctk.CTkButton(button_frame, text = truncate_text(text, 780), font = (main.FONT, 12, "normal"), anchor = "center", 
                                border_color = main.FADED_TEXT_COLOR, text_color = main.TEXT_COLOR, fg_color = main.BASE_COLOR,
                                border_width = 1, hover_color = main.ENTRY_COLOR, border_spacing = 8, 
                                command = lambda text = truncate_text(text, 780): open_detail(text))
         button.grid(row = index, column = 0, padx = 120, pady = 4, sticky = "nsew")

   # Function to change the color of the pressed button
   def change_button_color(button):
      global LAST_PRESSED

      # If there is a previously pressed button, reset its color
      if LAST_PRESSED is not None:
         LAST_PRESSED.configure(fg_color = main.BASE_COLOR, hover_color = main.ENTRY_COLOR, text_color = main.TEXT_COLOR, 
                                border_width = 1, border_color = main.FADED_TEXT_COLOR)

      # Change the color of the currently pressed button
      button.configure(fg_color = main.FG_COLOR, hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR,
                       border_width = 0, border_color = main.FRAME_COLOR)
      
      # Update the last pressed button to the current button
      LAST_PRESSED = button

   # Function to create pagination buttons
   def create_pagination(): 
      global CUR_PAGE

      # Remove all existing widgets in page frame
      for widget in page_frame.winfo_children(): 
         widget.destroy() 
      
      # Remove all existing widgets in page frame
      for widget in page_frame.winfo_children(): 
         widget.destroy() 
         
      total_pages = (len(RESULTS) + PAGE_SIZE - 1) // PAGE_SIZE 
      
      # Function to change the current page
      def change_page(page): 
         global CUR_PAGE, LAST_PRESSED
         
         CUR_PAGE = page 
         
         create_buttons(CUR_PAGE) 
         
      # Create a button for each page
      for index in range(1, total_pages + 1): 
         button = ctk.CTkButton(page_frame, text = str(index), font = (main.FONT, 12, "normal"), anchor = "center", border_color = main.FADED_TEXT_COLOR, 
                                text_color = main.TEXT_COLOR, fg_color = main.BASE_COLOR, border_width = 1, hover_color = main.ENTRY_COLOR, 
                                border_spacing = 4, command = lambda index = index: change_page(index)) 
         button.grid(row = 0, column = index, padx = 4, pady = 4, sticky="nsew")

         if index == 1:
            change_button_color(button)
         
         button.bind("<Button-1>", lambda event, button = button: change_button_color(button))

         page_frame.grid_columnconfigure(index, weight = 1)

   # Function to search for journals based on the query
   def search_journal(entry):
      global RESULTS, SEARCH, CUR_PAGE, LAST_PRESSED

      if LAST_PRESSED is not None:
         LAST_PRESSED = None

      button_frame.grid_forget()
      page_frame.grid_forget()

      loading_label.configure(text = "Looking for a match")
      loading_label.grid(row = 2, column = 0, padx = 0, pady = 0, sticky = "nsew")
      
      start_animation()

      query = entry.get()
      SEARCH = query

      try:
         # Try to run the researcheria function and get results
         RESULTS = asyncio.run(researcheria.researcheria(frame, query))
         CUR_PAGE = 1

         if len(RESULTS) == 0:
            stop_animation()  # Stop the animation 
            no_results_found(loading_label)  # Show a message indicating no results were found
         elif RESULTS is None:
            start_animation()  # Stop the animation 

            RESULTS = asyncio.run(researcheria.researcheria(frame, query))

            if len(RESULTS) == 0:
               stop_animation()
               no_results_found(loading_label)
            else:
               stop_animation()  # Stop the animation 
               create_buttons(CUR_PAGE)  # Create the buttons for the results

               if len(RESULTS) > 10:
                  create_pagination()  # Create the pagination buttons

               loading_label.grid_forget()  # Hide the loading label

               button_frame.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "nsew")
               page_frame.grid(row = 4, column = 0, padx = 160, pady = 0, sticky = "nsew")
         else:
            stop_animation()  # Stop the animation 
            create_buttons(CUR_PAGE) # Create the buttons for the results

            if len(RESULTS) > 10:
               create_pagination()  # Create the pagination buttons

            loading_label.grid_forget()  # Hide the loading label

            button_frame.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "nsew")
            page_frame.grid(row = 4, column = 0, padx = 160, pady = 0, sticky = "nsew")
      except Exception as e:
         search_journal(search_entry)
         SEARCH = None  # Stop the animation if the connection fails

         # Stop animation if an exception occurs
         stop_animation()

   # Function to start the search process
   def start_search(event = None):
      def check_internet_connection(url = "http://www.google.com/"):
         """
         This function checks the internet connection by sending an HTTP request to the provided URL.
         If the connection is successful, it will start a thread to run the 'search_journal' function.
         If the connection fails, it will show a popup message to check the internet connection.
         
         :param url: URL used to check the internet connection. Default is http://www.google.com/
         """

         global SEARCH

         try:
            response = requests.get(url, timeout = 5)  # Send an HTTP request with a timeout of 5 seconds
            query = search_entry.get()

            if SEARCH == query:
               return
            elif query == "" or query == "Search by title":
               popup.open_popup("Please fill in the search field", True)
               
               return
            elif response.status_code == 200 and not (query == "" or query == "Search by title"):
               # If the connection is successful, start a thread to run the 'search_journal' function
               thread = threading.Thread(target = search_journal, args = (search_entry,))

               thread.start()
            else:
               stop_animation()  # Stop the animation if the connection fails
               root.after(2000, loading_label.grid_forget())  # Hide the loading label after 2 seconds

               SEARCH = None  # Resets the values ​​of SEARCH

               # If the connection fails (status code is not 200), show a popup message
               popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

               return
         except requests.ConnectionError:
            stop_animation()  # Stop the animation if the connection fails
            root.after(2000, loading_label.grid_forget())  # Hide the loading label after 2 seconds

            SEARCH = None  # Resets the values ​​of SEARCH

            # If a connection error occurs, show a popup message
            popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)

            return

      # Call the function to check the internet connection
      check_internet_connection()

   # Create the search button
   search_button = ctk.CTkButton(search_frame, text = "Search", font = (main.FONT, 10, "bold"), fg_color = main.FG_COLOR,
                                 hover_color = main.FG_HOVER_COLOR, text_color = main.BASE_COLOR, width = 72, corner_radius = 16,
                                 command = lambda: start_search(search_entry))
   search_button.grid(row = 0, column = 1, padx = (8, 0), pady = 4, sticky = "nsew")

   # Bind the Return key to start the search
   search_entry.bind("<Return>", start_search)

   # Get the current children of the frame
   is_widget.WIDGETS = frame.winfo_children()
