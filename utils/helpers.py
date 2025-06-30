import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_price(search_results):
    try:
        # Mock data for testing
        mock_data = {
            "bricks": 8.0,  # ₹8 per brick in India (2025 estimate)
            "cement": 400.0,  # ₹400 per bag
            "steel": 60.0  # ₹60 per kg
        }
        material = search_results.get("query", "").lower().split("price of ")[1].split(" in")[0].strip()
        if material in mock_data:
            logger.info(f"Using mock price for {material}: {mock_data[material]}")
            return mock_data[material]

        # Extract price from Tavily API results
        for result in search_results.get("results", []):
            content = result.get("content", "").lower()
            # Look for INR prices (e.g., ₹8, 400 rupees, INR 60)
            price_match = re.search(r'(?:₹|inr|rs\.?)\s*(\d+\.?\d*)', content)
            if price_match:
                price = float(price_match.group(1))
                logger.info(f"Extracted price from content: {price}")
                return price
        logger.warning(f"No price found in search results for {material}")
        return None
    except Exception as e:
        logger.error(f"Error in extract_price: {str(e)}")
        return None

def extract_permits(search_results):
    try:
        permits = []
        # Mock data for testing
        mock_permits = {
            "mumbai": ["Building Permit", "NOC from Fire Department", "Municipal Approval"],
            "jaipur": ["Rajasthan Urban Development Approval", "Building Permit", "Environmental Clearance"]
        }
        location = search_results.get("query", "").lower().split("permits needed in ")[1].split(",")[0].strip()
        if location in mock_permits:
            logger.info(f"Using mock permits for {location}: {mock_permits[location]}")
            return ", ".join(mock_permits[location])

        # Extract permits from Tavily API results
        for result in search_results.get("results", []):
            content = result.get("content", "").lower()
            if "permit" in content or "approval" in content or "clearance" in content:
                permit_matches = re.findall(r'(building permit|noc|municipal approval|environmental clearance|urban development approval)', content)
                permits.extend(permit_matches)
        permits = list(set(permits))  # Remove duplicates
        logger.info(f"Extracted permits: {permits}")
        return ", ".join(permits) if permits else None
    except Exception as e:
        logger.error(f"Error in extract_permits: {str(e)}")
        return None

def extract_competitor_prices(search_results):
    try:
        prices = []
        # Mock data for testing
        mock_prices = {
            "residential construction": ["₹2000 per sqft (Contractor A)", "₹2100 per sqft (Contractor iunie, 2025: B)"],
            "commercial construction": ["₹2500 per sqft (Contractor X)", "₹2600 per sqft (Contractor Y)"]
        }
        project_type = search_results.get("query", "").lower().split("pricing for ")[1].strip()
        if project_type in mock_prices:
            logger.info(f"Using mock competitor prices for {project_type}: {mock_prices[project_type]}")
            return mock_prices[project_type]

        # Extract prices from Tavily API results
        for result in search_results.get("results", []):
            content = result.get("content", "").lower()
            price_match = re.findall(r'(?:₹|inr|rs\.?)\s*(\d+\.?\d*)\s*(per\s*\w+|\w+)', content)
            for price, unit in price_match:
                prices.append(f"₹{price} {unit}")
        prices = list(set(prices))  # Remove duplicates
        logger.info(f"Extracted competitor prices: {prices}")
        return prices if prices else ["No competitor pricing found"]
    except Exception as e:
        logger.error(f"Error in extract_competitor_prices: {str(e)}")
        return ["No competitor pricing found"]