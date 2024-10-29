import fitz  # PyMuPDF
import os
import text_preprocess

def extract_chunks_by_page(file_path):
    chunks = {}
    
    print(file_path)
    # Open the PDF file
    doc = fitz.open(file_path)

    for page_num in range(doc.page_count):
        page = doc[page_num]
        page_text = page.get_text()
        
        # Split page text roughly in half
        text_length = len(page_text)
        mid_point = text_length // 2
        
        # Find nearest period to split on
        split_index = page_text.find('.', mid_point)
        if split_index == -1:  # If no period found, just split at midpoint
            split_index = mid_point
        
        # Create two chunks per page
        chunk1 = page_text[:split_index+1].strip()
        chunk2 = page_text[split_index+1:].strip()
        
        chunks[f"page_{page_num+1}_chunk1"] = chunk1
        chunks[f"page_{page_num+1}_chunk2"] = chunk2

    doc.close()
    return chunks
