import psycopg2
from sentence_transformers import SentenceTransformer
from psycopg2.extras import RealDictCursor
import faiss
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# Load a pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use a different model if preferred


# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="307_text",     # Replace with your database name
    user="simon",            # Replace with your PostgreSQL username
    password=os.getenv("DB_PW"),        # Replace with your PostgreSQL password
    host="localhost",                # Replace with your host (e.g., "localhost" or your remote host address)
    port="5432"                      # Replace with your PostgreSQL port (default is 5432)
)

cursor = conn.cursor(cursor_factory=RealDictCursor)

# Execute a query to fetch all rows from the Chapters table
cursor.execute('SELECT * FROM Chapters')

# Fetch all the results
rows = cursor.fetchall()

title_embeddings = []
content_embeddings = []

# Print all rows
for row in rows:
    chapter_title = row['chapter_title']
    chapter_content = row['content']
    title_embeddings.append(model.encode(chapter_title))
    content_embeddings.append(model.encode(chapter_content))

title_embedding_matrix = np.array(title_embeddings).astype('float32')
content_embedding_matrix = np.array(content_embeddings).astype('float32')

title_dimension = title_embedding_matrix.shape[1]
content_dimension = content_embedding_matrix.shape[1]

title_index = faiss.IndexFlatL2(title_dimension)
title_index.add(title_embedding_matrix)
content_index = faiss.IndexFlatL2(content_dimension)
content_index.add(content_embedding_matrix)

print(f"Number of title vectors in Faiss index: {title_index.ntotal}")
print(f"Number of content vectors in Faiss index: {content_index.ntotal}")

# Save the title and content Faiss indices
faiss.write_index(title_index, 'title_vector_index.faiss')
faiss.write_index(content_index, 'content_vector_index.faiss')

print("Faiss indices saved to disk.")

