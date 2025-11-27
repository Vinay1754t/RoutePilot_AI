import requests
from langchain_core.tools import tool
import os

@tool
def get_current_weather(city: str):
    """
    Fetches the current weather for a specific city using OpenWeatherMap.
    Returns temperature (Celsius) and weather conditions.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeatherMap API Key is missing."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" # Returns Temp in Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            feels_like = data["main"]["feels_like"]
            return f"Current weather in {city}: {desc}, Temperature: {temp}°C (Feels like {feels_like}°C)."
        else:
            return f"Error fetching weather: {data.get('message', 'Unknown error')}"
            
    except Exception as e:
        return f"Error connecting to weather service: {str(e)}"
