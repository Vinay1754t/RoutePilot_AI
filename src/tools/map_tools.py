import folium
import os
import tempfile
from langchain_core.tools import tool
from geopy.geocoders import Nominatim

# Initialize Geolocator (Unique user_agent is required)
geolocator = Nominatim(user_agent="routepilot_map_agent")

@tool
def generate_trip_map(start_city: str, end_city: str):
    """
    Generates an interactive HTML map showing the route between two cities.
    Useful for visualizing the trip. Returns the file path of the map.
    """
    try:
        # 1. Get Coordinates
        loc_a = geolocator.geocode(start_city)
        loc_b = geolocator.geocode(end_city)
        
        if not loc_a or not loc_b:
            return "Error: Could not find one of the locations to map."

        coords_a = [loc_a.latitude, loc_a.longitude]
        coords_b = [loc_b.latitude, loc_b.longitude]

        # 2. Create Map (Centered between the two points)
        mid_lat = (coords_a[0] + coords_b[0]) / 2
        mid_lon = (coords_a[1] + coords_b[1]) / 2
        m = folium.Map(location=[mid_lat, mid_lon], zoom_start=4)

        # 3. Add Markers & Line
        folium.Marker(coords_a, popup=start_city, tooltip="Start").add_to(m)
        folium.Marker(coords_b, popup=end_city, tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)
        
        # Draw the line
        folium.PolyLine([coords_a, coords_b], color="blue", weight=3, opacity=0.7).add_to(m)

        # 4. Save to Temporary HTML File
        temp_dir = tempfile.gettempdir()
        filename = "map_route.html"
        file_path = os.path.join(temp_dir, filename)
        m.save(file_path)

        return f"Map generated successfully at {file_path}"

    except Exception as e:
        return f"Error creating map: {str(e)}"