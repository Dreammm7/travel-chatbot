A Retrieval-Augmented Generation (RAG) based chatbot API for travel agencies, built with FastAPI. It answers travel-related queries using a combination of structured data, FAQs, and trip itineraries, leveraging vector search and Google Gemini LLM for accurate, context-aware responses.

## Features
- **Conversational API** for travel-related queries
- **Retrieval-Augmented Generation (RAG):** Combines vector search with LLM for factual, context-based answers
- **Supports FAQs, trip details, and itineraries**
- **Powered by FastAPI** for easy deployment and scalability

## Data Sources
- `data/upcoming_trip.csv`: List of upcoming trips (name, destination, duration, price, etc.)
- `data/faqs.csv`: Frequently asked questions and answers
- `data/itineraries/`: Folder containing detailed itineraries as text files

## Setup
1. **Clone the repository**
2. **Install dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root directory
   - Add your Google API key:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     ```
4. **Run the API server:**
   ```bash
   uvicorn main:app --reload
   ```

## Usage
- Access the API at `http://localhost:8000/`
- Use the `/chat` endpoint to interact with the chatbot

### Example Request
```json
POST /chat
{
  "query": "Tell me about the Royal Rajasthan trip. What is the plan for Day 2?"
}
```

### Example Response
```json
{
  "response": "Day 2 of the Royal Rajasthan trip includes..."
}
```

## API Endpoints
- `GET /` — Welcome message
- `POST /chat` — Chat with the travel bot
  - Request body: `{ "query": "<your question>" }`
  - Response: `{ "response": "<AI answer>" }`

## Environment Variables
- `GOOGLE_API_KEY`: API key for Google Gemini (set in `.env`)

## License
MIT License 
