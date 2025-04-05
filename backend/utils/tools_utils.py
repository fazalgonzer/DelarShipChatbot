
import re
from dotenv import load_dotenv, find_dotenv
import os
import json


load_dotenv(find_dotenv())
JSON_PATH=os.getenv("JSON_PATH")
with open(JSON_PATH, 'r') as file:
    JSON_DATA = json.load(file)




def validate_date(date):
    """Validates if the date is in YYYY-MM-DD format."""
    print("Validating date:", date)
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) is not None

def validate_dealership_id(dealership_id):
    """Validates if the dealership ID exists in the JSON data."""
    
    return dealership_id in JSON_DATA["dealerships"]

def check_appointment_availability(dealership_id, date):
    """Returns available time slots for a given dealership and date."""
    if not validate_dealership_id(dealership_id) or not validate_date(date):
        return "Invalid dealership ID or date format"
    
    dealership = JSON_DATA["dealerships"][dealership_id]
    all_slots = dealership["available_slots"]  # Fetch predefined slots
    booked_slots = dealership.get("appointments", {}).get(date, [])
    
    return [slot for slot in all_slots if slot not in booked_slots]

def is_within_working_hours(dealership_id, date, requested_slots):
    """Checks if the total booked hours exceed the dealership's daily limit."""
    dealership = JSON_DATA["dealerships"][dealership_id]
    max_hours = dealership["max_hours"]
    booked_slots = dealership.get("appointments", {}).get(date, [])
    return len(booked_slots) + len(requested_slots) <= max_hours