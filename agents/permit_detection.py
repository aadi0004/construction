import logging
from apis.tavily_client import tavily_client
from utils.helpers import extract_permits

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def permit_detection_agent(state):
    logger.info(f"Permit detection agent received state: {state}")
    location = state.get("location", "")
    logger.info(f"Extracted location from state: {location}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"permits": "Error: Invalid state type", "error": f"Invalid state type: {type(state)}"}
    try:
        if not location:
            logger.error("No location provided for permit detection")
            return {"permits": "Error: Please provide a valid location in India", "error": "No location provided"}
        query = f"construction permits needed in {location}, India 2025"
        results = tavily_client.search(query)
        logger.info(f"Tavily API results for {query}: {results}")
        permits = extract_permits(results)
        if not permits:
            logger.error(f"No permits extracted for {location}")
            return {"permits": "No permit information found for India", "error": f"No permits found for {location}"}
        logger.info(f"Extracted permits for {location}: {permits}")
        return {"location": location, "permits": permits}
    except Exception as e:
        logger.error(f"Error in permit_detection_agent: {str(e)}")
        return {"permits": f"Error fetching permits: {str(e)}", "error": f"API error: {str(e)}"}