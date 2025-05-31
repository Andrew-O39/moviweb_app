import os
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = "http://www.omdbapi.com/"

def fetch_movie_details(title: str) -> dict | None:
    """
    Fetch movie details from the OMDb API based on the movie title.
    Args:
        title (str): The movie title to search for.
    Returns:
        dict or None: A dictionary of movie details if found, otherwise None.
    """

    if not OMDB_API_KEY:
        raise ValueError("OMDB_API_KEY is not set in environment variables.")

    params = {"t": title, "apikey": OMDB_API_KEY}

    try:
        response = requests.get(OMDB_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            # Movie not found
            return None

        # Extract year (handle ranges)
        year_raw = data.get("Year")
        year = None
        if year_raw:
            year = int(year_raw.split("–")[0])

        # Extract rating safely
        rating_raw = data.get("imdbRating")
        try:
            rating = float(rating_raw) if rating_raw and rating_raw != "N/A" else None
        except (ValueError, TypeError):
            rating = None

        return {
            "name": data.get("Title"),
            "director": data.get("Director"),
            "year": year,
            "rating": rating,
            "poster_url": data.get("Poster")
        }

    except requests.RequestException as e:
        # Log the error
        print(f"Error fetching movie data from OMDb API: {e}")
        return None