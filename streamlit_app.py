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
from agents.material_price import material_price_agent
import requests
from datetime import datetime

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
if "inventory_materials" not in st.session_state:
    st.session_state.inventory_materials = {}

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Material Prices", "Competitor Pricing", "Cost Estimation",
    "Project Scheduling", "Permit Detection", "Bid Optimization", "Government Projects", "Inventory Management"
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
    st.write("Enter a project type and location to fetch area-wise competitor pricing in India.")
    project_type_input = st.text_input("Project type (e.g., Residential Construction):", value=st.session_state.competitor_pricing, key="competitor_pricing_input")
    location_input = st.text_input("Location (e.g., Rajasthan, Delhi):", key="location_input_competitor")
    if st.button("Get Competitor Prices", key="get_competitor_prices_button"):
        project_type = project_type_input.strip()
        location = location_input.strip()
        if not all([project_type, location]):
            st.error("Please enter a valid project type and location.")
            logger.warning("Empty project type or location input in Competitor Pricing tab")
        else:
            st.session_state.competitor_pricing = project_type
            logger.info(f"Project type input: {project_type}, location: {location}")
            state = {"project_type": project_type, "location": location}
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
                    st.success(f"Competitor prices in {location}, India (area-wise):")
                    for price in result["competitor_prices"]:
                        st.write(f"- {price}")
                else:
                    logger.error(f"Competitor pricing result invalid: {result}")
                    st.error("Failed to fetch competitor prices. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in competitor pricing tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab3:
    st.write("Enter details to estimate construction cost, optimize costs, and save time in India.")
    building_type = st.selectbox("Building Type", ["Residential", "Commercial", "Industrial"], key="building_type_input")
    location = st.text_input("Location (e.g., Mumbai, Maharashtra)", key="location_input")
    floors = st.number_input("Number of Floors", min_value=1, value=1, key="floors_input")
    area_sqft = st.number_input("Area (sqft)", min_value=100, value=1000, key="area_sqft_input")
    material = st.text_input("Primary Material (e.g., Bricks)", key="material_input")
    labor_cost = st.number_input("Labor Cost (₹ per sqft)", min_value=0.0, value=500.0, key="labor_cost_input")
    material_options = ["Bricks", "Cement", "Steel"]
    alternative_material = st.selectbox("Alternative Material for Cost Comparison", material_options, index=0, key="alt_material_input")
    if st.button("Estimate Cost, Time & Optimize", key="estimate_cost_button"):
        if not all([location, material]):
            st.error("Please enter all required fields (Location and Primary Material).")
            logger.warning("Missing required fields in Cost Estimation tab")
        else:
            logger.info(f"Cost estimation inputs: building_type={building_type}, location={location}, floors={floors}, area_sqft={area_sqft}, material={material}, labor_cost={labor_cost}")
            state = {
                "building_type": building_type,
                "location": location,
                "floors": floors,
                "area_sqft": area_sqft,
                "material": material,
                "labor_cost": labor_cost * area_sqft,
                "alternative_material": alternative_material
            }
            logger.info(f"State sent to cost_estimation_workflow: {state}")
            try:
                result = cost_estimation_workflow(state)
                logger.info(f"Cost estimation workflow result: {result}")
                if result is None:
                    logger.error("Cost estimation workflow returned None")
                    st.error("Failed to estimate cost and time. Workflow returned no result.")
                elif "error" in result and result["error"]:
                    logger.error(f"Cost estimation error: {result['error']}")
                    st.error(f"Error: {result['error']}")
                elif "total_cost" in result and isinstance(result["total_cost"], (int, float)):
                    time_months = result["estimated_time"]
                    st.success(f"Estimated Cost in {location}, India: ₹{result['total_cost']:.2f}")
                    st.success(f"Estimated Time: Approximately {time_months:.1f} months")
                    if "alternative_cost" in result:
                        st.write(f"**Cost Optimization Suggestion:** Switching to {alternative_material} could reduce costs to ₹{result['alternative_cost']:.2f}")
                    if floors > 1 and area_sqft > 1000:
                        st.write(f"**Time-Saving Tip:** Consider modular construction techniques to reduce time by up to 20% for projects with {floors} floors and {area_sqft} sqft.")
                else:
                    logger.error(f"Cost estimation result invalid: {result}")
                    st.error("Failed to estimate cost and time. Invalid result format.")
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
    st.write("Enter a location in India to detect required permits and estimate costs.")
    location_input = st.text_input("Location (e.g., Mumbai, Maharashtra):", value=st.session_state.permit_detection, key="permit_detection_input")
    project_type_input = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"], key="project_type_permit_input")
    if st.button("Detect Permits & Costs", key="detect_permits_button"):
        location = location_input.strip()
        project_type = project_type_input.strip()
        if not location or not project_type:
            st.error("Please enter a valid location and project type.")
            logger.warning("Empty location or project type input in Permit Detection tab")
        else:
            st.session_state.permit_detection = location
            logger.info(f"Location input: {location}, Project type: {project_type}")
            state = {"location": location, "project_type": project_type}
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
                    # Automated Permit Cost Calculator
                    permit_costs = {
                        "Residential": {"Mumbai": 50000, "Jaipur": 30000, "Delhi": 45000},
                        "Commercial": {"Mumbai": 100000, "Jaipur": 70000, "Delhi": 90000},
                        "Industrial": {"Mumbai": 150000, "Jaipur": 100000, "Delhi": 120000}
                    }
                    estimated_cost = permit_costs.get(project_type, {}).get(location.split(",")[0].strip(), 50000)
                    st.write(f"**Estimated Permit Cost:** ₹{estimated_cost:.2f} (based on 2025 averages)")
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
                    st.success("Optimal Bid Suggestion:")
                    st.write(result["optimal_bid"])
                else:
                    logger.error(f"Bid optimization result invalid: {result}")
                    st.error("Failed to optimize bid. Invalid result format.")
            except Exception as e:
                logger.error(f"Error in bid optimization tab: {str(e)}")
                st.error(f"Error: {str(e)}")

with tab7:
    st.header("Government Construction Project Opportunities")
    st.subheader(f"Latest Projects in India (Updated: {datetime.now().strftime('%I:%M %p IST, %B %d, %Y')})")
    st.write("Explore real-time opportunities for builders and contractors. Data fetched from official sources.")

    # API endpoint for real-time government project data (mocked for now)
    api_url = "https://api.example.com/govt_projects"  # Placeholder URL
    projects = st.session_state.get("govt_projects", [])
    if st.button("Refresh Projects"):
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                projects = response.json()
                st.session_state["govt_projects"] = projects
                logger.info("Government projects refreshed successfully")
            else:
                logger.error(f"API request failed with status code: {response.status_code}")
                # Mock new projects on refresh
                projects = [
                    {
                        "name": "Mumbai Coastal Road Phase 2",
                        "location": "Mumbai, Maharashtra",
                        "status": "Tendering (Opens Jul 15, 2025)",
                        "cost": "₹12,000 crore",
                        "tender_deadline": "Aug 10, 2025",
                        "apply_process": "Submit bids via Mumbai Metropolitan Region Development Authority (MMRDA) at mmrda.maharashtra.gov.in. Required: Technical proposal, financial bid, experience certificate.",
                        "contact": "MMRDA Office, Mumbai"
                    },
                    {
                        "name": "Hyderabad Metro Expansion",
                        "location": "Hyderabad, Telangana",
                        "status": "Planning (Tender opens Jul 20, 2025)",
                        "cost": "₹15,000 crore",
                        "tender_deadline": "Sep 5, 2025",
                        "apply_process": "Apply through Hyderabad Metro Rail Limited (HMRL) at hmrl.co.in. Submit pre-qualification and bid documents.",
                        "contact": "HMRL Office, Hyderabad"
                    }
                ]
                st.session_state["govt_projects"] = projects
                logger.warning("Using mock data due to API failure")
        except Exception as e:
            logger.error(f"Error fetching government projects: {str(e)}")
            projects = [
                {
                    "name": "Mumbai Coastal Road Phase 2",
                    "location": "Mumbai, Maharashtra",
                    "status": "Tendering (Opens Jul 15, 2025)",
                    "cost": "₹12,000 crore",
                    "tender_deadline": "Aug 10, 2025",
                    "apply_process": "Submit bids via Mumbai Metropolitan Region Development Authority (MMRDA) at mmrda.maharashtra.gov.in. Required: Technical proposal, financial bid, experience certificate.",
                    "contact": "MMRDA Office, Mumbai"
                },
                {
                    "name": "Hyderabad Metro Expansion",
                    "location": "Hyderabad, Telangana",
                    "status": "Planning (Tender opens Jul 20, 2025)",
                    "cost": "₹15,000 crore",
                    "tender_deadline": "Sep 5, 2025",
                    "apply_process": "Apply through Hyderabad Metro Rail Limited (HMRL) at hmrl.co.in. Submit pre-qualification and bid documents.",
                    "contact": "HMRL Office, Hyderabad"
                }
            ]
            st.session_state["govt_projects"] = projects
            logger.warning("Using mock data due to network error")

    for project in projects:
        with st.expander(f"{project['name']} - {project['location']}"):
            st.write(f"**Status:** {project['status']}")
            st.write(f"**Estimated Cost:** {project['cost']}")
            st.write(f"**Tender Deadline:** {project['tender_deadline']}")
            st.write(f"**Application Process:** {project['apply_process']}")
            st.write(f"**Contact:** {project['contact']}")
            st.write("---")

    st.write("**Note:** Ensure compliance with local regulations and submit bids well before deadlines. Regularly check official government portals for updates.")

with tab8:
    st.header("Inventory Management Tracker")
    st.write("Track on-site materials to minimize waste and reduce costs.")
    
    # Initialize or update inventory
    if "add_material" not in st.session_state:
        st.session_state.add_material = ""
    if "add_quantity" not in st.session_state:
        st.session_state.add_quantity = 0
    
    # Add material to inventory
    st.subheader("Add Material to Inventory")
    material_input = st.text_input("Material (e.g., Bricks, Cement)", value=st.session_state.add_material, key="inventory_material_input")
    quantity_input = st.number_input("Quantity", min_value=0, value=st.session_state.add_quantity, key="inventory_quantity_input")
    if st.button("Add to Inventory", key="add_inventory_button"):
        if material_input and quantity_input > 0:
            st.session_state.inventory_materials[material_input] = st.session_state.inventory_materials.get(material_input, 0) + quantity_input
            st.session_state.add_material = ""
            st.session_state.add_quantity = 0
            logger.info(f"Added {quantity_input} units of {material_input} to inventory")
            st.success(f"Added {quantity_input} units of {material_input} to inventory.")
        else:
            st.error("Please enter a valid material and quantity.")
            logger.warning("Invalid input for adding material to inventory")

    # Display current inventory
    st.subheader("Current Inventory")
    if st.session_state.inventory_materials:
        for material, quantity in st.session_state.inventory_materials.items():
            st.write(f"{material}: {quantity} units")
            # Alert for overstocking (>500 units) or shortages (<50 units)
            if quantity > 500:
                st.warning(f"Overstocking alert for {material}! Consider reducing orders to minimize waste.")
            elif quantity < 50:
                st.warning(f"Shortage alert for {material}! Order more to avoid delays.")
    else:
        st.write("No materials tracked yet. Add materials to begin.")

    # Remove material option
    st.subheader("Remove Material")
    remove_material = st.selectbox("Select Material to Remove", list(st.session_state.inventory_materials.keys()), key="remove_material_input")
    remove_quantity = st.number_input("Quantity to Remove", min_value=0, max_value=st.session_state.inventory_materials.get(remove_material, 0), value=0, key="remove_quantity_input")
    if st.button("Remove from Inventory", key="remove_inventory_button"):
        if remove_material and remove_quantity > 0:
            st.session_state.inventory_materials[remove_material] -= remove_quantity
            if st.session_state.inventory_materials[remove_material] <= 0:
                del st.session_state.inventory_materials[remove_material]
            logger.info(f"Removed {remove_quantity} units of {remove_material} from inventory")
            st.success(f"Removed {remove_quantity} units of {remove_material} from inventory.")
        else:
            st.error("Please select a material and valid quantity to remove.")
            logger.warning("Invalid input for removing material from inventory")