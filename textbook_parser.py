import fitz  # PyMuPDF

def extract_chapters_by_font_size(file_path):
    chapters = {}
    current_chapter = None
    chapter_content = ""

    # Open the PDF file
    doc = fitz.open(file_path)

    # Define a threshold for what we consider a "large" font size
    large_font_threshold = 12  # Adjust this threshold based on your PDF's formatting

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]  # Extract text blocks

        for block in blocks:
            if "lines" in block:  # Only consider text blocks
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        font_size = span["size"]

                        # Check if the text has a larger font size, indicating a chapter title
                        if font_size >= large_font_threshold and text[0].isdigit():
                            if current_chapter:
                                chapters[current_chapter] = chapter_content.strip()

                            current_chapter = text
                            chapter_content = ""
                        elif current_chapter:
                            chapter_content += text + " "

    # Add the last chapter to the dictionary
    if current_chapter:
        chapters[current_chapter] = chapter_content.strip()

    doc.close()
    return chapters

# Example usage
file_path = 'first 5 lectures.pdf'  # Replace with your file path
chapters = extract_chapters_by_font_size(file_path)

# Save each chapter's content to a separate file (optional)
for chapter_title, content in chapters.items():
    filename = f"{chapter_title.replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(content)

    print(f"Saved {filename}")
