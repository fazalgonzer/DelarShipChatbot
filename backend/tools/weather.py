from langchain_core.tools import tool
import requests


# Getting the weather for api 
@tool
def get_weather(location:str="New York")->dict:
    """Get the weather for a location."""
    try:
        
        
        # Use Open-Meteo's geocoding API to get latitude and longitude
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&format=json"
        geocode_response = requests.get(geocode_url)
        
        if geocode_response.status_code == 200 and "results" in geocode_response.json():
            result = geocode_response.json()["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            
            # Fetch weather data from Open-Meteo
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()["current_weather"]
                
                return {"name": "get_weather", "output": {"temperature": f"{weather_data['temperature']} Celcius", "city": f"{location}", "windspeed": f"{weather_data['windspeed']} km/h"}}
            else:
                return {"name": "get_weather", "output": "Error fetching weather data"}
        else:
            return {"name": "get_weather", "output": "Error fetching location data"}
    except Exception as e:
        return {"name": "get_weather", "output": f"An error occurred in WeatherTool: {str(e)}"}