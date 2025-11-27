from langchain_core.tools import tool

@tool
def estimate_local_costs(city: str, travel_style: str, duration_days: int):
    """
    Estimates the cost of food and local travel based on the city tier and travel style.
    Inputs:
    - city: Name of the city
    - travel_style: 'Budget Backpacker', 'Luxury/Comfort', or 'Adventure/Nature'
    - duration_days: Number of days of the trip
    """
    base_rates = {
        "Budget Backpacker": 40,
        "Adventure/Nature": 80,
        "Luxury/Comfort": 200
    }
    
    expensive_cities = ["Paris", "New York", "London", "Zurich", "Tokyo", "Dubai"]
    multiplier = 1.5 if city in expensive_cities else 1.0
    
    daily_cost = base_rates.get(travel_style, 50) * multiplier
    total_est = daily_cost * int(duration_days)
    
    return (f"Estimated basic spending (Food + Local Travel) for {duration_days} days "
            f"in {city} as a {travel_style}: ${total_est:.2f} USD. "
            f"(Note: This excludes flights and accommodation).")
