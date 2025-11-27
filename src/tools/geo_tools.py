from langchain_core.tools import tool
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


geolocator = Nominatim(user_agent="routepilot_ai_agent")

@tool
def get_coordinates(city_name: str):
    """Get the latitude and longitude of a specific city."""
    try:
        location = geolocator.geocode(city_name)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
        return "City not found."
    except Exception as e:
        return f"Error finding city: {str(e)}"

@tool
def calculate_distance(city_a: str, city_b: str):
    """Calculate the distance (in km) between two cities to estimate travel time."""
    try:
        loc_a = geolocator.geocode(city_a)
        loc_b = geolocator.geocode(city_b)
        
        if loc_a and loc_b:
            coords_a = (loc_a.latitude, loc_a.longitude)
            coords_b = (loc_b.latitude, loc_b.longitude)
            distance = geodesic(coords_a, coords_b).kilometers
            return f"The distance between {city_a} and {city_b} is approx {distance:.2f} km."
        return "One or both cities could not be found."
    except Exception as e:
        return f"Error calculating distance: {str(e)}"
