import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cost_estimation_agent(state):
    logger.info(f"Cost estimation agent received state: {state}")
    building_type = state.get("building_type", "Residential")
    location = state.get("location", "")
    floors = state.get("floors", 1)
    area_sqft = state.get("area_sqft", 1000)
    material = state.get("material", "Bricks")
    labor_cost = state.get("labor_cost", 500.0 * area_sqft)
    alternative_material = state.get("alternative_material", "Bricks")
    logger.info(f"Extracted from state: building_type={building_type}, location={location}, floors={floors}, area_sqft={area_sqft}, material={material}, labor_cost={labor_cost}, alternative_material={alternative_material}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"total_cost": 0.0, "error": f"Invalid state type: {type(state)}"}
    try:
        if not all([location, material]):
            logger.error("Missing required fields for cost estimation")
            return {"total_cost": 0.0, "error": "Missing required fields (Location and Material)"}
        
        # Material prices per sqft (2025 India estimates)
        material_prices = {
            "Bricks": 8.0 / 100,  # ₹ per sqft
            "Cement": 4.0 / 100,  # ₹ per sqft
            "Steel": 6.0 / 100    # ₹ per sqft
        }
        alt_material_prices = {
            "Bricks": 8.0 / 100,
            "Cement": 4.0 / 100,
            "Steel": 6.0 / 100
        }

        # Base cost per sqft based on building type
        base_cost_per_sqft = {
            "Residential": 2000.0,
            "Commercial": 2500.0,
            "Industrial": 3000.0
        }
        base_cost = base_cost_per_sqft.get(building_type.lower(), 2000.0) * area_sqft

        # Total material cost
        material_cost = material_prices.get(material, 100.0 / 100) * area_sqft
        total_cost = base_cost + material_cost + labor_cost
        logger.info(f"Calculated total cost: {total_cost}")

        # Alternative material cost for optimization
        alt_material_cost = alt_material_prices.get(alternative_material, 100.0 / 100) * area_sqft
        alt_total_cost = base_cost + alt_material_cost + labor_cost
        logger.info(f"Alternative cost with {alternative_material}: {alt_total_cost}")

        # Estimate time (approx 1.5 months per 1000 sqft per floor)
        time_months = (floors * (area_sqft / 1000)) * 1.5
        logger.info(f"Estimated time: {time_months} months")

        return {
            "building_type": building_type,
            "location": location,
            "floors": floors,
            "area_sqft": area_sqft,
            "material": material,
            "labor_cost": labor_cost,
            "total_cost": total_cost,
            "estimated_time": time_months,
            "alternative_cost": alt_total_cost if alt_material != material else None
        }
    except Exception as e:
        logger.error(f"Error in cost_estimation_agent: {str(e)}")
        return {"total_cost": 0.0, "error": f"Calculation error: {str(e)}"}