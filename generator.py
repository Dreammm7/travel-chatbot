import google.generativeai as genai
from settings import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_response(context: str, query: str) -> str:
    """
    Generates a response using the Gemini model based on provided context and query.
    """
    # --- THIS IS THE NEW, IMPROVED PROMPT ---
    prompt = f"""
    You are 'TravelBot', an expert AI assistant for a travel agency. Your tone should be friendly, professional, and helpful.
    
    You MUST follow these rules:
    1.  Answer the user's query strictly based on the provided "Context".
    2.  Do not make up any information, prices, or policies that are not explicitly in the "Context".
    3.  If the "Context" does not contain the information needed to answer the query, you MUST say "I'm sorry, I don't have enough information to answer that question."
    
    Here is the information to use:
    
    Context:
    {context}
    
    ---
    
    User's Query:
    {query}
    
    Answer:
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up the response to remove potential markdown and extra whitespace
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating response: {e}")
        return "Sorry, I'm having trouble generating a response right now. Please try again later."