import faiss
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import psycopg2


# returns chapter
def retrieve_index(query):

    # Load the Faiss indices from disk
    index_title = faiss.read_index('title_vector_index.faiss')
    index_content = faiss.read_index('content_vector_index.faiss')

    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use a different model if preferred

    # Example query


    # Create an embedding for the query
    query_embedding = model.encode([query]).astype('float32')

    # Number of nearest neighbors to retrieve
    top_k = 1

    # Search for the top K most similar titles
    distances_title, indices_title = index_title.search(query_embedding, top_k)
    print(f"Indices of the most similar titles: {indices_title}")
    print(f"Distances to the most similar titles: {distances_title}")

    # Search for the top K most similar content
    distances_content, indices_content = index_content.search(query_embedding, top_k)
    print(f"Indices of the most similar contents: {indices_content}")
    print(f"Distances to the most similar contents: {distances_content}")

    # Define weights for title and content relevance
    title_weight = 0.5  # Adjust this weight based on importance
    content_weight = 0.5  # Adjust this weight based on importance

    # Combine results using weighted scoring
    combined_scores = {}

    # Combine title results
    for i, index in enumerate(indices_title[0]):
        if index in combined_scores:
            combined_scores[index] += title_weight * (1 / (1 + distances_title[0][i]))  # Normalize by distance
        else:
            combined_scores[index] = title_weight * (1 / (1 + distances_title[0][i]))

    # Combine content results
    for i, index in enumerate(indices_content[0]):
        if index in combined_scores:
            combined_scores[index] += content_weight * (1 / (1 + distances_content[0][i]))  # Normalize by distance
        else:
            combined_scores[index] = content_weight * (1 / (1 + distances_content[0][i]))

    # Sort the results by the combined score in descending order
    sorted_indices = sorted(combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True)

    # Retrieve and print the most relevant documents
    print("Top relevant chapters based on combined scoring:")
    for i in range(len(sorted_indices)):
        sorted_indices[i]+=1
        print(f"Chapter Number: {sorted_indices[i]}")
    return sorted_indices

def retrieve_text(query):
    chap_nums = retrieve_index(query)
    load_dotenv()
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="307_text",     # Replace with your database name
        user="simon",          # Replace with your PostgreSQL username
        password=os.getenv('DB_PW'),       # Replace with your PostgreSQL password
        host="localhost",      # Replace with your host (e.g., "localhost" or your remote host address)
        port="5432"            # Replace with your PostgreSQL port (default is 5432)
    )
    cursor = conn.cursor()
    content_list = []
    print(chap_nums)
    for chap_num in chap_nums:
        chap_num = int(chap_num)
        cursor.execute('SELECT content FROM Chapters WHERE chapter_number = %s', (chap_num,))
        content_list.append(cursor.fetchone())
    return content_list

# print(retrieve_text('what is combinatorics'))