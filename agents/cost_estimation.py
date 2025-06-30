import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cost_estimation_agent(state):
    logger.info(f"Cost estimation agent received state: {state}")
    material = state.get("material", "")
    quantity = state.get("quantity", 1)
    labor_cost = state.get("labor_cost", 0.0)
    price = state.get("price", 100.0)
    logger.info(f"Extracted from state: material={material}, quantity={quantity}, labor_cost={labor_cost}, price={price}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"total_cost": 0.0, "error": f"Invalid state type: {type(state)}"}
    try:
        if not material:
            logger.error("No material provided for cost estimation")
            return {"total_cost": 0.0, "error": "No material provided"}
        total_cost = (price * quantity) + labor_cost
        logger.info(f"Calculated total cost: {total_cost}")
        return {"material": material, "quantity": quantity, "labor_cost": labor_cost, "total_cost": total_cost}
    except Exception as e:
        logger.error(f"Error in cost_estimation_agent: {str(e)}")
        return {"total_cost": 0.0, "error": f"Calculation error: {str(e)}"}