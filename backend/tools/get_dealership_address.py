from langchain_core.tools import tool
from utils.tools_utils import validate_dealership_id
from dotenv import load_dotenv, find_dotenv
import os 
import json


load_dotenv(find_dotenv())

JSON_PATH=os.getenv("JSON_PATH")
with open(JSON_PATH, 'r') as file:
    JSON_DATA = json.load(file)





@tool    
def get_dealership_address(dealership_id: str="12345") -> dict:
    """Fetches the address of the given dealership."""
    try:
    
        if not validate_dealership_id(dealership_id):
            return {"name": "get_dealership_address","output": "Invalid dealership ID"}
        
        if dealership_id not in JSON_DATA.get("dealerships", {}):
            return {"name": "get_dealership_address","output": "Dealership not found"}
        
        if "address" not in JSON_DATA["dealerships"][dealership_id]:
            return {"name": "get_dealership_address", "output": "Address not found"}
        
        return {"name": "get_dealership_address", "output": JSON_DATA["dealerships"][dealership_id]["address"]}
    except Exception as e:
        return {"name": "get_dealership_address", "output": f"An error occurred: {str(e)}"}

