import logging
from apis.tavily_client import tavily_client
from utils.helpers import extract_competitor_prices

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def competitor_pricing_agent(state):
    logger.info(f"Competitor pricing agent received state: {state}")
    project_type = state.get("project_type", "")
    logger.info(f"Extracted project_type from state: {project_type}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"competitor_prices": ["Error: Invalid state type"], "error": f"Invalid state type: {type(state)}"}
    try:
        if not project_type:
            logger.error("No project type provided for competitor pricing")
            return {"competitor_prices": ["Error: Please provide a valid project type"], "error": "No project type provided"}
        query = f"competitor pricing for {project_type} in India 2025"
        results = tavily_client.search(query)
        logger.info(f"Tavily API results for {query}: {results}")
        prices = extract_competitor_prices(results)
        logger.info(f"Extracted competitor prices for {project_type}: {prices}")
        return {"project_type": project_type, "competitor_prices": prices}
    except Exception as e:
        logger.error(f"Error in competitor_pricing_agent: {str(e)}")
        return {"competitor_prices": ["Error fetching competitor prices"], "error": f"API error: {str(e)}"}