import requests
import json

# NASA POWER API URL
BASE_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

def get_climate_data(lat, lon, start_year=2000, end_year=2022):
    params = {
        "parameters": "T2M,PRECTOT,RH2M,ALLSKY_SFC_SW_DWN", 
        # ------ PARAMETERS USED -------
        # T2M : Temperature (°C)
        # PRECTOT : Precipitation (mm/ day)
        # RH2M : Humidity (%)
        # ALLSKY_SFC_SW_DWN : Light Intensity (MJ/m²/day)
        # ----- USEFUL PARAMETERS ------
        # T2M_MAX : Maximum temperature in day (°C)
        # T2M_MIN : Minumum temperature in day (°C)
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2))  # Print full response for debugging
    except json.JSONDecodeError:
        print("Error: API did not return valid JSON.")
        return None
    
    if "properties" not in data:
        print(f"Error: 'properties' not found in API response. Check parameters.")
        return None

# Example Call
get_climate_data(51.5, -0.12)
