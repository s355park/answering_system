import psycopg2
import json
import os 
from dotenv import load_dotenv

load_dotenv()

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="307_text",     # Replace with your database name
    user="simon",            # Replace with your PostgreSQL username
    password=os.getenv('DB_PW'),        # Replace with your PostgreSQL password
    host="localhost",                # Replace with your host (e.g., "localhost" or your remote host address)
    port="5432"                      # Replace with your PostgreSQL port (default is 5432)
)

cursor = conn.cursor()

# Create the Chapters table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Chapters (
    id SERIAL PRIMARY KEY,
    chapter_number INTEGER,
    chapter_title TEXT,
    content TEXT
)
''')

# Commit changes
conn.commit()
parsed_data = None
# Open and read the JSON file
with open('preprocessed_text.json', 'r') as file:
    parsed_data = json.load(file)

for key, value in parsed_data.items():
    chapter_title = ""
    chapter_text = ""
    for i in range(len(value)):
        if value[i].isdigit():
            chapter_title = chapter_title[:-1]
            chapter_text = value[i:]
            break
        chapter_title+=value[i]
    cursor.execute('''
    INSERT INTO chapters (chapter_number, chapter_title, content)
    VALUES (%s, %s, %s)
    ''', (key, chapter_title, chapter_text))
    conn.commit()

    

# Close the cursor and the connection
cursor.close()




conn.close()
