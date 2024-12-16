# Importing necessary libraries
from openai import OpenAI

# Function to run the model
def colleriaai(prompt):
    """
    This function contains the algorithm for running 
    the GPT-4o AI model on which ColleriaAI is based
    """

    # Open the file in read-binary mode
    # Note that it should be "rb" for reading, not "wb" for writing
    with open("model/key.bin", "rb") as file:
        api_key = file.read()  # Read the API key from the file
        api_key = api_key.decode("utf-8")

        file.close()

    # Configure the OpenAI client with the base URL and API key
    client = OpenAI(base_url = "https://api.zukijourney.com/v1", 
                    api_key = api_key)

    # Create a chat completion using the specified model and prompt
    response = client.chat.completions.create(
        model = "gpt-4o", 
        messages = [{"role": "user", "content": prompt}]
    )

    # Return the content of the first response choice
    return response.choices[0].message.content
