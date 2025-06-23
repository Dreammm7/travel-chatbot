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
    You are TravelBot, a helpful and friendly AI assistant for a travel agency.

    Your behavior rules are as follows:
    Always provide helpful, polite, and informative responses to any travel-related query, including questions about destinations, planning, packing, travel tips, etc.
    For any query that requires factual information (such as attractions, prices, schedules, or policies), answer strictly based on the provided "Context".
    Do not invent or assume any specific data (like prices, schedules, or destinations) that is not present in the "Context".
    If the required information is not found in the "Context", respond with: "I'm sorry, I don't have enough information to answer that question."
    
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