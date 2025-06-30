import logging
from apis.gemini_client import generate_content

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def project_scheduling_agent(state):
    logger.info(f"Project scheduling agent received state: {state}")
    project_details = state.get("project_details", "")
    logger.info(f"Extracted project_details from state: {project_details}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"schedule": "Error: Invalid state type", "error": f"Invalid state type: {type(state)}"}
    try:
        if not project_details:
            logger.error("No project details provided for scheduling")
            return {"schedule": "Error: Please provide valid project details", "error": "No project details provided"}
        prompt = f"Generate a project schedule for: {project_details}"
        schedule = generate_content(prompt)
        logger.info(f"Generated schedule: {schedule}")
        return {"project_details": project_details, "schedule": schedule}
    except Exception as e:
        logger.error(f"Error in project_scheduling_agent: {str(e)}")
        return {"schedule": f"Error generating schedule: {str(e)}", "error": f"API error: {str(e)}"}