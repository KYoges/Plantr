import requests
import pandas as pd


def get_plant_distribution(plant_name):
    """Fetches location data for a plant from GBIF"""
    url = f"https://api.gbif.org/v1/occurrence/search?scientificName={plant_name}&limit=1000"
    response = requests.get(url)
    data = response.json()
    
    locations = []
    for record in data["results"]:
        if "decimalLatitude" in record and "decimalLongitude" in record:
            locations.append({
                "scientificName": record.get("scientificName"),
                "latitude": record.get("decimalLatitude"),
                "longitude": record.get("decimalLongitude"),
                "country": record.get("country"),
                "year": record.get("year"),
                "month": record.get("month"),
                "day": record.get("day"),
            })
    
    return locations
