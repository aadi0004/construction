import os
import httpx
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def google_search(query):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        logger.error("SERPER_API_KEY is missing")
        return {}
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query}
    try:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Serper API error: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error in Serper API: {str(e)}")
        return {}