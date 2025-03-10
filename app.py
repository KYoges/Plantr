from flask import Flask, render_template, jsonify, request, redirect, url_for
import threading
import time
import os
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import great_circle
from llm_api.llm_integration import get_plant_info_llm, make_sch_info
import pandas as pd
from price_pred_api.get_yield import *
import json
import markdown
from llm_api.filterCrops import filter_crops
from flask_cors import CORS
from ics import Calendar
import folium
import pgeocode
import math
geolocator = Nominatim(user_agent="plantr")

ICS_FILE_PATH = "crop_growth_calendar.ics"
CSV_FILE = "llm_api/combined_crop_distribution.csv"
nomi = pgeocode.Nominatim('us')


# FLASK CONFIG
app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'),
            static_folder=os.path.join(os.getcwd(), 'frontend', 'static'))

CORS(app)

print(os.path.join(os.getcwd(), 'frontend', 'static'))

# DATAFRAMES
df = pd.read_csv("llm_api/us_crop_species_distribution.csv")
df2 = pd.read_csv("llm_api/us_crop_species_distribution2.csv")
df_crop_distribution = pd.read_csv(CSV_FILE)


df_yield = pd.read_csv('ml_model/yield_data_with_scientific_names.csv')
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'))



def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Function to compute the three nearest plants from a DataFrame
def get_nearest_plants(df, user_lat, user_lon, k=3):
    # Compute distance for each record
    df['distance'] = df.apply(lambda row: haversine_distance(user_lat, user_lon, row['latitude'], row['longitude']), axis=1)
    # Sort by distance and take the top k
    nearest_df = df.sort_values(by='distance').head(k)
    return nearest_df.to_dict(orient='records')


# STANDALONE FUNCTIONS
def generate_data():
    response = get_plant_info_llm(choice)
    time.sleep(5)
    return response

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


# ROUTES


# DATA APIS



@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/get-plant-yield')
def get_plant_yield():
    crop_scientific_name = 'Zea mays'
    crop_scientific_name = crop_scientific_name.replace(" ","_").lower()
    predicted_yield = get_yield_for_crop_and_country(df_yield, "India", crop_scientific_name)
    lower_price,upper_price = get_yield_lower_upper_price(predicted_yield,crop_scientific_name,2)
    print(lower_price,upper_price)
    return render_template('    -display.html', predicted_yield=predicted_yield, lower_price=lower_price, upper_price=upper_price)

# @app.route('/start_task')
# def start_task():
#     thread = threading.Thread(target=generate_data)
#     thread.start()
#     return jsonify({'status': 'Task started'})

@app.route('/loading-screen')
def loading_screen():
    plant_name = request.args.get('plant_name', '')
    return render_template('loading-sceen.html', plant_name=plant_name)

@app.route('/markdown-page')
def markdown_page():
    return render_template('chatbox.html')

@app.route('/markdown')
def get_llm_markdown():
    choice = 'Zea mays'
    llm_response = get_plant_info_llm(choice)
    md_text = markdown.markdown(llm_response)
    return jsonify({"markdown":md_text})

@app.route('/redirect_after_delay')
def redirect_after_delay():
    time.sleep(2) 
    return redirect(url_for('main_page'))

@app.route('/main_page')
def main_page():

    return render_template('index.html')

@app.route('/save-coordinates', methods=['POST'])
def save_coordinates():
    data = request.json

    df = pd.read_csv("llm_api/us_crop_species_distribution.csv")
    df2 = pd.read_csv("llm_api/us_crop_species_distribution2.csv")

    longitude = float(data.get("longitude"))
    latitude = float(data.get("latitude"))

    crops = filter_crops(df, latitude, longitude) 
    crops2 = filter_crops(df2, latitude, longitude) 

    with open('coordinates.json', 'w') as file:
        json.dump(data, file)

    global list_crops
    list_crops = (crops+crops2)

    return jsonify({"message": "Coordinates saved successfully"})

@app.route('/get_list', methods=['GET'])
def get_list():
    return jsonify(list_crops)

@app.route("/get-events", methods=["GET"])
def get_events():
    try:
        # Read the ICS file
        with open(ICS_FILE_PATH, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())

        # Parse events
        events = []
        for event in calendar.events:
            events.append({
                "title": event.name,
                "start": event.begin.isoformat(),
                "end": event.end.isoformat() if event.end else event.begin.isoformat(),
            })

        return jsonify(events)

    except FileNotFoundError:
        return jsonify({"error": "ICS file not found"}), 404
@app.route("/calendar")
def get_calender():
    return render_template("calender.html")
@app.route('/get-info')
def get_info_plant():
    return render_template('chatbox.html')

@app.route('/predict', methods=['GET'])
def predict():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Missing location. Please provide a location."}), 400

    crops = predict_crop(location)

    return jsonify({"recommended_crops": crops})


@app.route('/choose', methods=['POST'])
def choose():
    data = request.get_json()
    location = data.get("location")
    choice = data.get("choice")

    if not location or not choice:
        return jsonify({"error": "Invalid location or choice"}), 400

    return jsonify(user_choice(location, choice))

from urllib.parse import unquote

@app.route('/dashboard')
def dashboard():
    import pandas as pd
    from ics import Calendar
    import markdown

    # --- 1. Get Map Data from CSV ---
    # Get the URL parameter and decode it
    plant_name = request.args.get('plant_name', 'Zea mays L.')
    plant_name = unquote(plant_name)  # Decodes any URL-encoded characters

    df = pd.read_csv(CSV_FILE)
    df = df[df["scientificName"].str.contains(plant_name, case=False, na=False)]
    if df.empty:
        return f"<h1>No data found for {plant_name}</h1>", 404
    df = df.dropna(subset=["latitude", "longitude"])
    plant_data = df[["latitude", "longitude", "scientificName", "country", "year"]].to_dict(orient="records")

    # --- 2. Get Calendar Events from ICS File ---
    events = []
    try:
        with open("calendar.ics", "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())
        for event in calendar.events:
            events.append({
                "title": event.name,
                "start": event.begin.isoformat(),
                "end": event.end.isoformat() if event.end else event.begin.isoformat(),
            })
    except FileNotFoundError:
        events = []

    # --- 3. Get Plant Information (Markdown via LLM) ---
    choice = plant_name.split()[0]
    llm_response = get_plant_info_llm(choice)  # Assume this function is defined elsewhere
    md_text = markdown.markdown(llm_response)

    # --- 4. Get Yield Information ---
    crop_scientific_name = plant_name.split()[0]
    crop_scientific_name_url = crop_scientific_name.replace(" ", "_").lower()

    predicted_yield = get_yield_for_crop_and_country(df_yield, "India", crop_scientific_name_url)
    lower_price, upper_price = get_yield_lower_upper_price(predicted_yield, crop_scientific_name_url, 2)

    return render_template(
        "main.html",
        plant_data=plant_data,
        events=events,
        markdown=md_text,
        predicted_yield=predicted_yield,
        lower_price=lower_price,
        upper_price=upper_price
    )

@app.route("/process_input" , methods=['POST'])
def process_input():
    postcode = request.form.get('postcode')
    location = geolocator.geocode(f"{postcode}, USA")
    if not location:
        return jsonify({"status": "error", "message": "Invalid or unknown postcode."}), 400

    latitude = location.latitude
    longitude = location.longitude

   
    # Calculate the three nearest plants
    plant_options = get_nearest_plants(df_crop_distribution, latitude, longitude, k=3)

    return jsonify({
        "status": "success",
        "postcode": postcode,
        "latitude": latitude,
        "longitude": longitude,
        "plant_options": plant_options
    })




if __name__ == "__main__":
    app.run(debug=True)

