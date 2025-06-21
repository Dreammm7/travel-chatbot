from fastapi import FastAPI
from pydantic import BaseModel
from data_loader import load_knowledge_base
from retriever import create_vector_store, query_vector_store
from generator import generate_response

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

print("---Loading Knowledge Base---")
trips_df, faqs_df, itineraries = load_knowledge_base()
print("---Knowledge Base Loaded---")

create_vector_store(trips_df,faqs_df,itineraries)


app= FastAPI(
    title="Travel Agency Chatbot API",
    decription="An api for a RAG-based travel chatbot.",
    version="1.0.0",
)

@app.get("/")
async def read_root():
    """
    A welcome message for the API root.
    """
    return {"message":"Welcome to the Travel Chatbot API!"}

@app.post("/chat", response_model=ChatResponse)
async def chat_handler(request: ChatRequest):
    """
    Handles chat requests by querying the vector store and generating a response.
    """
    # 1. Retrieve context from the vector store
    context_from_db = query_vector_store(request.query, n_results=3)
    context_str = "\n---\n".join(context_from_db)

    print(f"\n[DEBUG] Context being sent to LLM:\n{context_str}\n")

    # 2. Generate a response using the LLM
    ai_response = generate_response(context=context_str, query=request.query)

    # 3. Return the response
    return ChatResponse(response=ai_response)

# from retriever import query_vector_store
# from generator import generate_response

# print("\n---Running a Test Query---")
# test_query= "Tell me about the Royal Rajasthan trip. What is the plan for Day 2?"
# context_from_db = query_vector_store(test_query, n_results=3)

# context_str ="\n---\n".join(context_from_db)

# print(f"Context being sent to LLM:\n{context_str}")

# ai_response = generate_response(context=context_str, query=test_query)

# print(f"\n---AI Generated Response---")
# print(ai_response)
# print("-----------------------------\n")