# retriever.py

import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

# 1. Initialize a ChromaDB client
client = chromadb.Client()

# 2. Initialize the Sentence Transformer model
# This model will be downloaded from the internet the first time it's used.
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Create a ChromaDB collection (like a table in a traditional database)
# We have to define our own embedding function to use sentence-transformers
class MyEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        batch_embeddings = embedding_model.encode(input)
        return batch_embeddings.tolist()

embedding_function = MyEmbeddingFunction()

try:
    print("--- Resetting Vector Store ---")
    client.delete_collection(name="travel_info")
except Exception as e:
    print(f"--- No existing collection to reset, or another error: {e} ---")

collection = client.get_or_create_collection(
    name="travel_info",
    embedding_function=embedding_function
)

# 4. Function to create and populate the vector store
def create_vector_store(trips_df: pd.DataFrame, faqs_df: pd.DataFrame, itineraries: dict):
    print("--- Creating Vector Store ---")
    
    documents = []
    metadatas = []
    ids = []
    
    # Process Trips
    for index, row in trips_df.iterrows():
        doc = (f"Trip Name: {row['trip_name']}. Destination: {row['destination_city']}, {row['destination_state']}. "
               f"Duration: {row['duration_days']} days. Price: INR {row['price_inr']}.")
        documents.append(doc)
        metadatas.append({'source': 'trips', 'trip_id': row['trip_id']})
        ids.append(f"trip_{row['trip_id']}")

    # Process FAQs
    for index, row in faqs_df.iterrows():
        # Combine the question and answer into a single document for better context
        doc = f"Question: {row['question']}\nAnswer: {row['answer']}"
        documents.append(doc)
        # The metadata now just needs to point to the source
        metadatas.append({'source': 'faqs'})
        ids.append(f"faq_{index}")
    
    for filename, content in itineraries.items():
        trip_id = filename.replace('_itinerary.txt', '')
        documents.append(content)
        metadatas.append({'source': 'itineraries', 'trip_id': trip_id})
        ids.append(f"itinerary_{trip_id}")

    # Add all documents to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("--- Vector Store Created Successfully ---")

# 5. Function to query the vector store
def query_vector_store(query: str, n_results: int = 3) -> list:
    """
    Queries the vector store for the most relevant documents.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]