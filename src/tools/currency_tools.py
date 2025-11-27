import requests
import os
from langchain_core.tools import tool

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str):
    """
    Converts a specific amount from one currency to another using live exchange rates.
    Example input: amount=100, from_currency='USD', to_currency='INR'
    """
    api_key = os.environ.get("EXCHANGERATE_API_KEY")
    if not api_key:
        return "Error: ExchangeRate API Key is missing."
    
    # Using ExchangeRate-API 
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data["result"] == "success":
            converted_amount = data["conversion_result"]
            rate = data["conversion_rate"]
            return (f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency} "
                    f"(Exchange Rate: 1 {from_currency} = {rate:.2f} {to_currency}).")
        else:
            return f"Error converting currency: {data.get('error-type', 'Unknown error')}"
            
    except Exception as e:
        return f"Error connecting to currency service: {str(e)}"
