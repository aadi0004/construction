import streamlit as st
import logging
from langgraph_workflow import (
    material_price_workflow,
    competitor_pricing_workflow,
    cost_estimation_workflow,
    project_scheduling_workflow,
    permit_detection_workflow,
    bid_optimization_workflow
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.title("Construction Assistant for Builders & Contractors")

# Initialize session state for input persistence
if "material_price" not in st.session_state:
    st.session_state.material_price = ""
if "competitor_pricing" not in st.session_state:
    st.session_state.competitor_pricing = ""
if "cost_material" not in st.session_state:
    st.session_state.cost_material = ""
if "project_scheduling" not in st.session_state:
    st.session_state.project_scheduling = ""
if "permit_detection" not in st.session_state:
    st.session_state.permit_detection = ""
if "bid_optimization" not in st.session_state:
    st.session_state.bid_optimization = ""

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Material Prices", "Competitor Pricing", "Cost Estimation",
    "Project Scheduling", "Permit Detection", "Bid Optimization"
])

with tab1:
    st.write("Enter a construction material to fetch its current price in India (INR).")
    material_input = st.text_input("Material name (e.g., Bricks, Cement, Steel):", value=st.session_state.material_price, key="material_price_input")
    if st.button("Get Price", key="get_price_button"):
        material = material_input.strip()
        if not material:
            st.error("Please enter a valid material name.")
            logger.warning("Empty material input in Material Prices tab")
        else:
            st.session_state.material_price = material
            logger.info(f"Material input: {material}")
            state = {"material": material}
            logger.info(f"State sent to material_price_workflow: {state}")
            try:
                result = material_price_workflow(state)
                logger.info(f"Material price workflow result: {result}")
                if result is None:
                    logger.error("Material price workflow returned None")
                    st.error("Failed to fetch material price. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Material price error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "price" in result and isinstance(result["price"], (int, float)):
                    st.success(f"Current price of {material} in India: ₹{result['price']:.2f}")
                else:
                    logger.error(f"Material price result invalid: {result}")
                    st.error("Failed to fetch material price. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in material price tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab2:
    st.write("Enter a project type to fetch competitor pricing in India.")
    project_type_input = st.text_input("Project type (e.g., Residential Construction):", value=st.session_state.competitor_pricing, key="competitor_pricing_input")
    if st.button("Get Competitor Prices", key="get_competitor_prices_button"):
        project_type = project_type_input.strip()
        if not project_type:
            st.error("Please enter a valid project type.")
            logger.warning("Empty project type input in Competitor Pricing tab")
        else:
            st.session_state.competitor_pricing = project_type
            logger.info(f"Project type input: {project_type}")
            state = {"project_type": project_type}
            logger.info(f"State sent to competitor_pricing_workflow: {state}")
            try:
                result = competitor_pricing_workflow(state)
                logger.info(f"Competitor pricing workflow result: {result}")
                if result is None:
                    logger.error("Competitor pricing workflow returned None")
                    st.error("Failed to fetch competitor prices. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Competitor pricing error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "competitor_prices" in result and isinstance(result["competitor_prices"], list):
                    st.success("Competitor prices in India:")
                    for price in result["competitor_prices"]:
                        st.write(f"- {price}")
                else:
                    logger.error(f"Competitor pricing result invalid: {result}")
                    st.error("Failed to fetch competitor prices. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in competitor pricing tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab3:
    st.write("Enter material details to estimate project cost in India.")
    cost_material_input = st.text_input("Material name (e.g., Bricks):", value=st.session_state.cost_material, key="cost_material_input")
    quantity = st.number_input("Quantity:", min_value=1, value=1)
    labor_cost = st.number_input("Labor cost (₹):", min_value=0.0, value=500.0)
    if st.button("Estimate Cost", key="estimate_cost_button"):
        material = cost_material_input.strip()
        if not material:
            st.error("Please enter a valid material name.")
            logger.warning("Empty material input in Cost Estimation tab")
        else:
            st.session_state.cost_material = material
            logger.info(f"Cost estimation inputs: material={material}, quantity={quantity}, labor_cost={labor_cost}")
            state = {"material": material, "quantity": quantity, "labor_cost": labor_cost}
            logger.info(f"State sent to cost_estimation_workflow: {state}")
            try:
                result = cost_estimation_workflow(state)
                logger.info(f"Cost estimation workflow result: {result}")
                if result is None:
                    logger.error("Cost estimation workflow returned None")
                    st.error("Failed to estimate cost. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Cost estimation error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "total_cost" in result and isinstance(result["total_cost"], (int, float)):
                    st.success(f"Total estimated cost in India: ₹{result['total_cost']:.2f}")
                else:
                    logger.error(f"Cost estimation result invalid: {result}")
                    st.error("Failed to estimate cost. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in cost estimation tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab4:
    st.write("Enter project details to generate a schedule.")
    project_details_input = st.text_area("Project details (e.g., Build a 2000 sqft house in Mumbai):", value=st.session_state.project_scheduling, key="project_scheduling_input")
    if st.button("Generate Schedule", key="generate_schedule_button"):
        project_details = project_details_input.strip()
        if not project_details:
            st.error("Please enter valid project details.")
            logger.warning("Empty project details input in Project Scheduling tab")
        else:
            st.session_state.project_scheduling = project_details
            logger.info(f"Project details input: {project_details}")
            state = {"project_details": project_details}
            logger.info(f"State sent to project_scheduling_workflow: {state}")
            try:
                result = project_scheduling_workflow(state)
                logger.info(f"Project scheduling workflow result: {result}")
                if result is None:
                    logger.error("Project scheduling workflow returned None")
                    st.error("Failed to generate schedule. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Project scheduling error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "schedule" in result:
                    st.success("Project Schedule:")
                    st.write(result["schedule"])
                else:
                    logger.error(f"Project scheduling result invalid: {result}")
                    st.error("Failed to generate schedule. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in project scheduling tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab5:
    st.write("Enter a location in India to detect required construction permits.")
    location_input = st.text_input("Location (e.g., Mumbai, Maharashtra):", value=st.session_state.permit_detection, key="permit_detection_input")
    if st.button("Detect Permits", key="detect_permits_button"):
        location = location_input.strip()
        if not location:
            st.error("Please enter a valid location in India.")
            logger.warning("Empty location input in Permit Detection tab")
        else:
            st.session_state.permit_detection = location
            logger.info(f"Location input: {location}")
            state = {"location": location}
            logger.info(f"State sent to permit_detection_workflow: {state}")
            try:
                result = permit_detection_workflow(state)
                logger.info(f"Permit detection workflow result: {result}")
                if result is None:
                    logger.error("Permit detection workflow returned None")
                    st.error("Failed to detect permits. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Permit detection error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "permits" in result:
                    st.success(f"Required permits in {location}, India:")
                    st.write(result["permits"])
                else:
                    logger.error(f"Permit detection result invalid: {result}")
                    st.error("Failed to detect permits. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in permit detection tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab6:
    st.write("Enter project data to optimize your bid.")
    project_data_input = st.text_area("Project data (e.g., Build a 2000 sqft house in Mumbai):", value=st.session_state.bid_optimization, key="bid_optimization_input")
    if st.button("Optimize Bid", key="optimize_bid_button"):
        project_data = project_data_input.strip()
        if not project_data:
            st.error("Please enter valid project data.")
            logger.warning("Empty project data input in Bid Optimization tab")
        else:
            st.session_state.bid_optimization = project_data
            logger.info(f"Project data input: {project_data}")
            state = {"project_data": project_data}
            logger.info(f"State sent to bid_optimization_workflow: {state}")
            try:
                result = bid_optimization_workflow(state)
                logger.info(f"Bid optimization workflow result: {result}")
                if result is None:
                    logger.error("Bid optimization workflow returned None")
                    st.error("Failed to optimize bid. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Bid optimization error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "optimal_bid" in result:
                    st.success("Optimal bid suggestion:")
                    st.write(result["optimal_bid"])
                else:
                    logger.error(f"Bid optimization result invalid: {result}")
                    st.error("Failed to optimize bid. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in bid optimization tab: {str(e)}")
                st.error(f"Error: {str(e)}")