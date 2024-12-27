# Importing necessary libraries
from groq import Groq
import colleriaai_frame as caf
import is_widget

# Load model
MODEL = "llama-3.1-70b-versatile"
MODEL_NAME = MODEL.replace("-", " ").title()

# Declare global variable FRAME
FRAME = None

# Function to run the model
def colleriaai(frame, prompt):
    """
    This function contains the algorithm for running 
    the Llama 3.1 70B Versatile AI model on which 
    the ColleriaAI is based
    """

    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(frame): 
        return  # If the frame is destroyed, exit the function

    # Configure the Groq client with the API key
    client = Groq(api_key = caf.KEY)

    # Create a chat completion using the specified model and prompt
    response = client.chat.completions.create(
        model = MODEL, 
        messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )

    # Removed markdown punctuation in response
    response = response.choices[0].message.content
    response = response.replace("*", "").replace("#", "").replace("`", "")

    # Return the content of the first response choice
    return response
