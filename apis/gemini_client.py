import os
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini client
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_client = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("Gemini client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Gemini client: {str(e)}")
    gemini_client = None

def generate_content(prompt):
    if gemini_client is None:
        logger.error("Gemini client not initialized")
        return "Error: Gemini client not available"
    try:
        response = gemini_client.generate_content(prompt)
        logger.info(f"Gemini API response for prompt '{prompt}': {response.text}")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating content with Gemini: {str(e)}")
        return f"Error: {str(e)}"