import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import great_circle

# Load the merged dataset
df = pd.read_csv("llm_api/us_crop_species_distribution.csv")
df2 = pd.read_csv("llm_api/us_crop_species_distribution2.csv")

def filter_crops(df, lat, lon, radius_km=50):  # Increased radius
    # Convert latitude & longitude to NumPy arrays for vectorized calculations
    latitudes = df["latitude"].to_numpy()
    longitudes = df["longitude"].to_numpy()
    months = df["month"].to_numpy()
    scientific_names = df["scientificName"].to_numpy()

    current_month = datetime.now().month

    # Compute distances using NumPy (vectorized great-circle distance)
    locations = np.column_stack((latitudes, longitudes))
    distances = np.array([great_circle((lat, lon), tuple(loc)).km for loc in locations])

    # Filter crops within the radius and in the current month
    mask = (distances <= radius_km) & (months == current_month)

    # Get unique crop names (vectorized)
    unique_crops = np.unique(scientific_names[mask])

    return unique_crops.tolist()

# Example usage
latitude, longitude = 27.36, -82.54  # Example coordinates
crops = filter_crops(df, latitude, longitude) 
crops2 = filter_crops(df2, latitude, longitude) 
print(crops+crops2)
