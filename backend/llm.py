from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import os 

#Import the tools from the tools directory
from tools.weather import get_weather
from tools.check_appointment_availability import check_appointment_availability
from tools.get_dealership_address import get_dealership_address
from tools.schedule_appointment import schedule_appointment




load_dotenv(find_dotenv())
GROQ_API_KEY=os.getenv("GROQ_API_KEY") # e.g. "sk-..." or "pk-..." 
# or "g-..." depending on the type of key you have
MODEL_NAME=os.getenv("MODEL_NAME") # e.g. "gpt-4-turbo" or "gpt-3.5-turbo"

llm  = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)


llmWithTools=llm.bind_tools([get_weather, check_appointment_availability, get_dealership_address, schedule_appointment])  # Bind the tools to the LLM instance    

