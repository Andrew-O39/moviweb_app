import requests
import os
from dotenv import load_dotenv

OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = "http://www.omdbapi.com/"

load_dotenv()

def fetch_movie_details(title):
    """Fetch movie details from OMDb API by title."""
    if not OMDB_API_KEY:
        raise ValueError("OMDB_API_KEY is not set in environment variables.")

    params = {
        "t": title,
        "apikey": OMDB_API_KEY
    }

    try:
        response = requests.get(OMDB_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            return None  # Movie not found

        # Return only the relevant fields your app uses
        return {
            "name": data.get("Title"),
            "director": data.get("Director"),
            "year": data.get("Year"),
            "rating": data.get("imdbRating"),
            "poster_url": data.get("Poster")
        }

    except requests.RequestException as e:
        print(f"Error fetching movie data: {e}")
        return None