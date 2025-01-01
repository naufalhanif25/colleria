# Importing necessary libraries and modules
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import is_widget

# Declare global variable FRAME
FRAME = None

# Function to summarize text
def flassencia(frame, text, language = "english", length = 10):
    """
    This function is used to summarize long text into 
    shorter ones with support for many languages.
    """
    
    global FRAME

    FRAME = frame  # Assign the frame to the global variable FRAME

    # Check if frame is destroyed if 
    if is_widget.is_exist(FRAME): 
        return  # If the frame is destroyed, exit the function
    
    # Initialize the list of results
    RESULTS = []
    
    # Check if the language is Indonesian
    if language == "indonesian":
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function
    
        # Initialize Indonesian stemmer using Sastrawi
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        # Custom class for Indonesian stemmer to be callable
        class IndonesianStemmer:
            def __init__(self, stemmer):
                self.stemmer = stemmer

            def __call__(self, word):
                return self.stemmer.stem(word)

        # Custom class for Indonesian tokenizer
        class IndonesianTokenizer(Tokenizer):
            def __init__(self, language = "english"):
                super().__init__(language)

            def to_words(self, text):
                return text.split()

        # Use the custom Indonesian tokenizer and stemmer
        tokenizer = IndonesianTokenizer()
        indonesian_stemmer = IndonesianStemmer(stemmer)
        summarizer = LsaSummarizer(indonesian_stemmer)
        summarizer.stop_words = get_stop_words("english")  # Use English stop words as a workaround
    else: 
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function
        
        # Use default tokenizer and stemmer for the specified language
        tokenizer = Tokenizer(language) 
        summarizer = LsaSummarizer() 
        summarizer.stop_words = get_stop_words(language)

    # Parse the input text using the selected tokenizer
    parser = PlaintextParser.from_string(text, tokenizer)
    
    # Generate the summary with the specified length
    summary = summarizer(parser.document, length)

    # Collect the sentences of the summary
    for sentence in summary:
        # Check if frame is destroyed if 
        if is_widget.is_exist(FRAME): 
            return  # If the frame is destroyed, exit the function
        
        RESULTS.append(str(sentence))
        
    return "\n".join(RESULTS)  # Return the summary as a single string
