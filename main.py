from textbook_parser import extract_chunks_by_page
from text_preprocess import clean_math_text, tokenize_and_lemmatize
from embedding import create_faiss_indices
from retrieve import retrieve_index
import pickle
import os
def main():
    file_path = 'Database System Concepts 6th edition.pdf'  # Replace with your file path
    chunks = extract_chunks_by_page(file_path)

    # Create a dictionary to temporarily keep the processed content
    processed_chunks = []

    # Process each chunk's content and store it in the dictionary
    # chunk_name will be in format "page_X_chunkY" where X is page number and Y is 1 or 2
    for chunk_name, content in chunks.items():
        # Process the content using functions from text_preprocess
        cleaned_content = clean_math_text(content)
        processed_content = tokenize_and_lemmatize(cleaned_content)
        
        # Store the processed content in the dictionary
        processed_chunks.append(processed_content)

    print("preprocessing done")


    # Save the processed_chunks as a CSV file

    with open('chunks.pkl', 'wb') as f:
        pickle.dump(processed_chunks, f)
    
    create_faiss_indices(processed_chunks)

if __name__ == "__main__":
    main()

