import os
import httpx
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class TavilyClient:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"

    def search(self, query):
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"api_key": self.api_key, "query": query}
            with httpx.Client() as client:
                response = client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Tavily API error: {str(e)}")
            return {}

tavily_client = TavilyClient()