import faiss
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import psycopg2
import pickle

# returns chapter
def retrieve_index(query):

    # Load the Faiss index from disk
    index_content = faiss.read_index('content_vector_index.faiss')

    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use a different model if preferred

    # Create an embedding for the query
    query_embedding = model.encode([query]).astype('float32')

    # Number of nearest neighbors to retrieve
    top_k = 5

    # Search for the top K most similar content
    distances_content, indices_content = index_content.search(query_embedding, top_k)
    print(f"Indices of the most similar contents: {indices_content}")
    print(f"Distances to the most similar contents: {distances_content}")

    # Sort the results by distance in ascending order
    # Create pairs of (index, distance) and sort by distance
    pairs = list(zip(indices_content[0], distances_content[0]))
    sorted_pairs = sorted(pairs, key=lambda x: x[1])  # Sort by distance
    sorted_indices = [idx for idx, _ in sorted_pairs]  # Keep as index
    return sorted_indices

def retrieve_text(query):
    indicies = retrieve_index(query)
    with open('chunks.pkl', 'rb') as f:
        processed_chunks = pickle.load(f)
    selected_chunks = [processed_chunks[i] for i in indicies]
    return selected_chunks

# print(retrieve_text('what is combinatorics', content_list))