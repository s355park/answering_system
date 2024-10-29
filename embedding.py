from sentence_transformers import SentenceTransformer
import faiss
import numpy as np



def create_faiss_indices(chunks):
    # Load a pre-trained embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use a different model if preferred
    content_embeddings = []

    # Process each chunk
    for content in chunks:
        content_embeddings.append(model.encode(content))

    content_embedding_matrix = np.array(content_embeddings).astype('float32')
    content_dimension = content_embedding_matrix.shape[1]

    content_index = faiss.IndexFlatL2(content_dimension)
    content_index.add(content_embedding_matrix)

    print(f"Number of content vectors in Faiss index: {content_index.ntotal}")

    # Save the content Faiss index
    faiss.write_index(content_index, 'content_vector_index.faiss')

    print("Faiss index saved to disk.")
