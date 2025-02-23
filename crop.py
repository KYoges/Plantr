from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim, great_circle
import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import great_circle
from llm_integration import get_plant_info_llm, make_sch_info

df = pd.read_csv("llm_api/us_crop_species_distribution.csv")
df2 = pd.read_csv("llm_api/us_crop_species_distribution2.csv")

def get_location(postcode):
    geoLocator = Nominatim(user_agent="cropPrediction")
    location = geoLocator.geocode(postcode + ", USA")

    if location:
        return location.latitude, location.longitude
    return None, None  

def predict_crop(postcode):
    lat, lon = get_location(postcode)

    if lat is None or lon is None:
        return {"error": "Invalid postcode or geolocation failed"}

    return get_best_crops(lat, lon)

def user_choice(postcode, choice):
    crops = predict_crop(postcode)

    if "error" in crops:
        return crops  

    if choice not in crops:
        return {"error": "Invalid crop selection"}

    llm_response = query_llm(choice)

    return {"selected_crop": choice, "llm_response": llm_response}

def query_llm(choice):
    get_plant_info_llm(choice)
    make_sch_info(choice)

def get_best_crops(df, lat, lon, radius_km=50):
    latitudes = df["latitude"].to_numpy()
    longitudes = df["longitude"].to_numpy()
    months = df["month"].to_numpy()
    scientific_names = df["scientificName"].to_numpy()

    current_month = datetime.now().month

    locations = np.column_stack((latitudes, longitudes))
    distances = np.array([great_circle((lat, lon), tuple(loc)).km for loc in locations])

    mask = (distances <= radius_km) & (months == current_month)

    unique_crops = np.unique(scientific_names[mask])

    return unique_crops.tolist()

    

