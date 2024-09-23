import text_preprocess as tp
import json
import psycopg2

cleaned_text_dict = dict()
# change these constants to need
NUM_CHAP = 7
for i in range(1, NUM_CHAP+1):
    # Open the text file in read mode ('r')
    file_contents = ""
    with open(f'{i}.txt', 'r') as file:
    # Read the contents of the file
        file_contents = file.read()
    clean_text = tp.clean_math_text(file_contents)
    lemmatized_text = tp.tokenize_and_lemmatize(clean_text)
    cleaned_text_dict[i] = lemmatized_text
    # cleaned_text_dict[i] = clean_text

with open('preprocessed_text.json', 'w') as json_file:
    json.dump(cleaned_text_dict, json_file, indent=4)  # Use indent for pretty-printing

