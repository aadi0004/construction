import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def permit_detection_agent(state):
    logger.info(f"Permit detection agent received state: {state}")
    location = state.get("location", "")
    project_type = state.get("project_type", "Residential")
    logger.info(f"Extracted from state: location={location}, project_type={project_type}")
    if not isinstance(state, dict):
        logger.error(f"Invalid state type: {type(state)}")
        return {"permits": "Error: Invalid state type", "error": f"Invalid state type: {type(state)}"}
    try:
        if not location:
            logger.error("No location provided for permit detection")
            return {"permits": "Error: Please provide a valid location", "error": "No location provided"}
        
        # Mock permit data based on location and project type
        permit_data = {
            "Mumbai, Maharashtra": {
                "Residential": ["Building Permit", "Environmental Clearance", "Fire Safety NOC"],
                "Commercial": ["Building Permit", "Trade License", "Environmental Clearance", "Fire Safety NOC"],
                "Industrial": ["Building Permit", "Industrial License", "Environmental Clearance", "Fire Safety NOC", "Pollution Control Board Approval"]
            },
            "Jaipur, Rajasthan": {
                "Residential": ["Building Permit", "Water Supply NOC", "Fire Safety NOC"],
                "Commercial": ["Building Permit", "Trade License", "Water Supply NOC", "Fire Safety NOC"],
                "Industrial": ["Building Permit", "Industrial License", "Water Supply NOC", "Fire Safety NOC", "Pollution Control Board Approval"]
            },
            "Delhi, Delhi": {
                "Residential": ["Building Permit", "Sanitation NOC", "Fire Safety NOC"],
                "Commercial": ["Building Permit", "Trade License", "Sanitation NOC", "Fire Safety NOC"],
                "Industrial": ["Building Permit", "Industrial License", "Sanitation NOC", "Fire Safety NOC", "Pollution Control Board Approval"]
            }
        }
        location_key = next((k for k in permit_data.keys() if k in location), "Mumbai, Maharashtra")
        permits = permit_data.get(location_key, {}).get(project_type, ["General Building Permit"])
        logger.info(f"Detected permits for {location}, {project_type}: {permits}")
        return {"location": location, "project_type": project_type, "permits": permits}
    except Exception as e:
        logger.error(f"Error in permit_detection_agent: {str(e)}")
        return {"permits": f"Error detecting permits: {str(e)}", "error": f"API error: {str(e)}"}