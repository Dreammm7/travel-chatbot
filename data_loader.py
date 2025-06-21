import pandas as pd
from pathlib import Path

def load_knowledge_base():
    """
    Loads all the data from  the /data directory into memory.
    """
    data_path = Path(__file__).parent / "data"
    trips_df = pd.read_csv(data_path / "upcoming_trip.csv")
    faqs_df = pd.read_csv(data_path / "faqs.csv")

    itineraries ={}
    itinerary_path = data_path/ "itineraries"
    for file_path in itinerary_path.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            itineraries[file_path.name] = f.read()

    return trips_df, faqs_df, itineraries