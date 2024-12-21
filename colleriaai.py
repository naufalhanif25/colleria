# Importing necessary libraries
from groq import Groq

# Load model
MODEL = "llama-3.3-70b-versatile"
MODEL_NAME = MODEL.replace("-", " ").title()

# Function to run the model
def colleriaai(prompt):
    """
    This function contains the algorithm for running 
    the Llama 3.3 70B Instruct Turbo AI model on which 
    the ColleriaAI is based
    """

    # Open the file in read-binary mode
    # Note that it should be "rb" for reading, not "wb" for writing
    with open("model/key.bin", "rb") as file:
        api_key = file.read()  # Read the API key from the file
        api_key = api_key.decode("utf-8")

        file.close()

    # Configure the OpenAI client with the base URL and API key
    client = Groq(api_key = api_key)

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
