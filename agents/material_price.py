import logging
from apis.tavily_client import tavily_client
from utils.helpers import extract_price

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def material_price_agent(state):
    logger.info(f"Material price agent received state: {state}")
    material = state.get("material", "")
    logger.info(f"Extracted material from state: {material}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"price": 100.0, "error": f"Invalid state type: {type(state)}"}
    try:
        if not material:
            logger.error("No material provided for price lookup")
            return {"price": 100.0, "error": "No material provided"}
        query = f"current price of {material} in India 2025"
        results = tavily_client.search(query)
        logger.info(f"Tavily API results for {query}: {results}")
        price = extract_price(results)
        if price is None:
            logger.error(f"No price extracted for {material}")
            return {"price": 100.0, "error": f"No price found for {material}"}
        logger.info(f"Extracted price for {material}: {price}")
        return {"material": material, "price": price}
    except Exception as e:
        logger.error(f"Error in material_price_agent: {str(e)}")
        return {"price": 100.0, "error": f"API error: {str(e)}"}