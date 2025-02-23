import pandas as pd
import json
def get_yield_for_crop_and_country(yield_df, country, crop_scientific_name):
    country_col = f'Country_{country}'  
    crop_col = crop_scientific_name.lower()  
    
    if crop_col not in yield_df.columns or country_col not in yield_df.columns:
        print(f"Error: Column for country '{country}' or crop '{crop_scientific_name}' not found.")
        return None

    filtered_df = yield_df[
        (yield_df[country_col] == 1) & (yield_df[crop_col] == 1)
    ]
    
    if not filtered_df.empty:
        return filtered_df['hg/ha_yield'].values[0]
    else:
        print(f"No data found for crop '{crop_scientific_name}' in country '{country}'.")
        return None

def get_yield_lower_upper_price(yield_value, scientific_name, land_area_hectares):
    # Load price range data from a JSON file
    with open('avg_prices.json', 'r') as file:
        data = json.load(file)

    if scientific_name in data:
        price_range = data[scientific_name]
        lower_price = price_range['lower_end']
        higher_price = price_range['higher_end']

        total_yield = yield_value * land_area_hectares
        
        lower_total = total_yield * lower_price
        higher_total = total_yield * higher_price

        # Return the revenue range (lower and higher)
        return lower_total, higher_total
    else:
        print(f"Price data for '{scientific_name}' not found.")
        return None, None
