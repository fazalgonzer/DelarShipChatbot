from langchain_core.tools import tool
from utils.tools_utils import validate_dealership_id, validate_date
from dotenv import load_dotenv, find_dotenv
import os 
import json
load_dotenv(find_dotenv())
JSON_PATH=os.getenv("JSON_PATH")
with open(JSON_PATH, 'r') as file:
    JSON_DATA = json.load(file)



@tool
def check_appointment_availability(dealership_id:str="12345", date:str="2023-11-04")->dict:
    """Returns available time slots for a given dealership and date."""
    try:
        # Validate inputs
       
        
        if not validate_dealership_id(dealership_id) or not validate_date(date):
            
        
            return {"name":"check_appointment_availability","status":"fail","output":"Invalid dealership ID or date format"}
        

        
    
        dealership = JSON_DATA["dealerships"][dealership_id]

        
        all_slots = dealership["available_slots"]  # Fetch predefined slots
        booked_slots = dealership.get("appointments", {}).get(date, [])

    
        return {"name":"check_appointment_availability","output":f"Availible Slots:{[slot for slot in all_slots if slot not in booked_slots]}"}
    except Exception as e:
        return {"name":"check_appointment_availability","status":"fail","output":f"An error occurred: {str(e)}"}