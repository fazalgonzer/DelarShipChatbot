from langchain_core.tools import tool
from utils.tools_utils import validate_dealership_id, validate_date ,is_within_working_hours
from utils.date_utils import random_date
from dotenv import load_dotenv, find_dotenv
import json
import os 
load_dotenv(find_dotenv())

JSON_PATH=os.getenv("JSON_PATH")
with open(JSON_PATH, 'r') as file:
    JSON_DATA = json.load(file)











@tool
def schedule_appointment(user_id: str="user123", dealership_id="12345", date=None, requested_slots=["09:00", "10:00"], car_model="Toyota Camry") -> dict:
    """Books an appointment if the slots are available and within working hours."""
    try:
        print(date)
        if date is None or "2024-09-16":
            date = random_date()
            
        # Validate inputs
        if not all([
            isinstance(user_id, str),
            validate_dealership_id(dealership_id),
            validate_date(date),
            isinstance(car_model, str),
            isinstance(requested_slots, list) and all(isinstance(slot, str) for slot in requested_slots)
        ]):
            return {"name": "schedule_appointment", "status": "fail", "output": "Invalid input format"}

        # Check if dealership exists
        dealership = JSON_DATA["dealerships"].get(dealership_id)
        if not dealership:
            return {"name": "schedule_appointment", "status": "fail", "output": "Dealership not found"}
        
        # Initialize available slots for this date if not already set
        available_slots_per_day = dealership.setdefault("available_slots_per_day", {})
        if date not in available_slots_per_day:
            available_slots_per_day[date] = list(dealership["available_slots"])  # Copy default slots

        available_slots = available_slots_per_day[date]

        # Check if slots are available
        if not available_slots:
            return {"name": "schedule_appointment", "status": "fail", "output": "No available slots for this date"}

        # If requested slots are not available, show available slots
        if not all(slot in available_slots for slot in requested_slots):
            return {
                "name": "schedule_appointment",
                "status": "fail",
                "output": f"One or more time slots not available. Available slots: {available_slots}"
            }

        # Check max booking hours
        max_hours = dealership.get("max_hours", 5)
        booked_slots = len(dealership.setdefault("appointments", {}).setdefault(date, []))
        
        if booked_slots + len(requested_slots) > max_hours:
            return {
                "name": "schedule_appointment",
                "status": "fail",
                "output": f"Exceeds max booking hours per day. Available slots: {available_slots}"
            }

        # Check working hours
        if not is_within_working_hours(dealership_id, date, requested_slots):
            return {
                "name": "schedule_appointment",
                "status": "fail",
                "output": f"Exceeds dealership's working hours. Available slots: {available_slots}"
            }

        # Add appointment and update available slots for this date
        dealership["appointments"][date].extend(requested_slots)
        available_slots_per_day[date] = [slot for slot in available_slots if slot not in requested_slots]
        with open(JSON_PATH, 'w') as file:
            json.dump(JSON_DATA, file, indent=4)

        return {
        "name": "schedule_appointment",
        "status": "success",
        "output": {"status":"Appointment confirmed","details": {
            "user_id": user_id,
            "dealership_id": dealership_id,
            "date": date,
            "time_slots": requested_slots,
            "car_model": car_model
        }}
        
    }
       
    
    
        
    except Exception as e:
        return {
            "name": "schedule_appointment",
            "status": "fail",
            "output": f"An error occurred: {str(e)}"
        }
