import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Step 1: Normalize the Text
def clean_math_text(extracted_text):
    # Convert text to lowercase to maintain uniformity (optional)
    # cleaned_text = extracted_text.lower()
    
    # Remove special characters, keeping numbers and mathematical symbols
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s\+\-\=\>\<\(\)\/\*\.,]', '', extracted_text)
    
    return cleaned_text

# Step 2: Tokenization and Lemmatization (if needed)
def tokenize_and_lemmatize(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Reconstruct the cleaned text
    cleaned_text = ' '.join(lemmatized_tokens)
    return cleaned_text

# # Example usage:
# extracted_text = "Extracted text from the PDF file goes here with numbers 123 and symbols like +, -, =, >, <, etc."
# cleaned_text = clean_math_text(extracted_text)
# cleaned_text = tokenize_and_lemmatize(cleaned_text)
# print(cleaned_text)
