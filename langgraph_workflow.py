from langgraph.graph import StateGraph, END
from agents.material_price import material_price_agent
from agents.competitor_pricing import competitor_pricing_agent
from agents.cost_estimation import cost_estimation_agent
from agents.project_scheduling import project_scheduling_agent
from agents.permit_detection import permit_detection_agent
from agents.bid_optimization import bid_optimization_agent
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define state schema
from typing import Dict, Any

class State(Dict[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault("material", "")
        self.setdefault("price", 100.0)
        self.setdefault("project_type", "")
        self.setdefault("competitor_prices", ["No data"])
        self.setdefault("quantity", 1)
        self.setdefault("labor_cost", 0.0)
        self.setdefault("total_cost", 0.0)
        self.setdefault("project_details", "")
        self.setdefault("schedule", "No schedule")
        self.setdefault("location", "")
        self.setdefault("permits", "No permit information")
        self.setdefault("project_data", "")
        self.setdefault("optimal_bid", "No bid suggestion")
        self.setdefault("error", None)

# Simplified workflow execution to bypass LangGraph issues
def run_workflow(agent_func, state):
    logger.info(f"Running workflow with agent {agent_func.__name__} and state: {state}")
    state = State(state) if isinstance(state, dict) else State()
    result = agent_func(state)
    logger.info(f"Workflow result: {result}")
    return result if isinstance(result, dict) else {"error": f"Invalid result from {agent_func.__name__}"}

# Workflow definitions
material_price_workflow = lambda state: run_workflow(material_price_agent, state)
competitor_pricing_workflow = lambda state: run_workflow(competitor_pricing_agent, state)
project_scheduling_workflow = lambda state: run_workflow(project_scheduling_agent, state)
permit_detection_workflow = lambda state: run_workflow(permit_detection_agent, state)
bid_optimization_workflow = lambda state: run_workflow(bid_optimization_agent, state)

# Cost Estimation workflow (requires material price first)
def cost_estimation_workflow(state):
    logger.info(f"Running cost estimation workflow with state: {state}")
    state = State(state) if isinstance(state, dict) else State()
    material_result = material_price_agent(state)
    logger.info(f"Material price result for cost estimation: {material_result}")
    if isinstance(material_result, dict) and "error" not in material_result:
        state.update(material_result)
        result = cost_estimation_agent(state)
        logger.info(f"Cost estimation result: {result}")
        return result if isinstance(result, dict) else {"error": "Invalid result from cost_estimation_agent"}
    logger.error(f"Material price error in cost estimation: {material_result.get('error', 'Unknown error')}")
    return material_result