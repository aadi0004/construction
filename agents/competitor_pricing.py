import logging
from apis.tavily_client import tavily_client
from utils.helpers import extract_competitor_prices

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def competitor_pricing_agent(state):
    logger.info(f"Competitor pricing agent received state: {state}")
    project_type = state.get("project_type", "")
    location = state.get("location", "").lower()
    logger.info(f"Extracted project_type from state: {project_type}, location: {location}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"competitor_prices": ["Error: Invalid state type"], "error": f"Invalid state type: {type(state)}"}
    try:
        if not all([project_type, location]):
            logger.error("No project type or location provided for competitor pricing")
            return {"competitor_prices": ["Error: Please provide a valid project type and location"], "error": "No project type or location provided"}
        query = f"competitor pricing for {project_type} construction projects in {location} India 2025 area-wise"
        results = tavily_client.search(query)
        logger.info(f"Tavily API results for {query}: {results}")
        prices = extract_competitor_prices(results)
        if not prices or all("no competitor pricing" in p.lower() for p in prices):
            # Realistic mock data for builders, area-wise for Rajasthan and Delhi
            mock_prices = {
                "residential construction": {
                    "rajasthan": [
                        "₹2200 per sqft (ABC Builders, Jaipur)",
                        "₹2250 per sqft (XYZ Construction, Jodhpur)",
                        "₹2300 per sqft (PQR Developers, Udaipur)"
                    ],
                    "delhi": [
                        "₹2400 per sqft (LMN Enterprises, New Delhi)",
                        "₹2450 per sqft (RST Contractors, Gurgaon)",
                        "₹2500 per sqft (JKL Builders, Noida)"
                    ]
                },
                "commercial construction": {
                    "rajasthan": [
                        "₹2800 per sqft (MNO Contractors, Jaipur)",
                        "₹2850 per sqft (STU Builders, Kota)",
                        "₹2900 per sqft (VWX Developers, Jaisalmer)"
                    ],
                    "delhi": [
                        "₹3000 per sqft (PQR Enterprises, Delhi)",
                        "₹3050 per sqft (XYZ Contractors, Faridabad)",
                        "₹3100 per sqft (ABC Builders, Ghaziabad)"
                    ]
                }
            }
            prices = mock_prices.get(project_type.lower(), {}).get(location, ["No realistic competitor pricing data available for this area"])
            logger.info(f"Using mock competitor prices for {project_type} in {location}: {prices}")
        return {"project_type": project_type, "location": location, "competitor_prices": prices}
    except Exception as e:
        logger.error(f"Error in competitor_pricing_agent: {str(e)}")
        return {"competitor_prices": ["Error fetching competitor prices"], "error": f"API error: {str(e)}"}