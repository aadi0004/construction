import logging
from apis.gemini_client import generate_content

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def bid_optimization_agent(state):
    logger.info(f"Bid optimization agent received state: {state}")
    project_data = state.get("project_data", "")
    logger.info(f"Extracted project_data from state: {project_data}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"optimal_bid": "Error: Invalid state type", "error": f"Invalid state type: {type(state)}"}
    try:
        if not project_data:
            logger.error("No project data provided for bid optimization")
            return {"optimal_bid": "Error: Please provide valid project data", "error": "No project data provided"}
        prompt = f"Provide a realistic bid optimization suggestion for a builder or contractor for the following project in India 2025: {project_data}. Include a total bid amount in INR, a breakdown of costs (materials, labor, overhead), and a competitive margin suggestion."
        optimal_bid = generate_content(prompt)
        logger.info(f"Generated optimal bid: {optimal_bid}")
        return {"project_data": project_data, "optimal_bid": optimal_bid}
    except Exception as e:
        logger.error(f"Error in bid_optimization_agent: {str(e)}")
        return {"optimal_bid": f"Error optimizing bid: {str(e)}", "error": f"API error: {str(e)}"}