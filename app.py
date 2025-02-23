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

# FLASK CONFIG
app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'),
            static_folder=os.path.join(os.getcwd(), 'frontend', 'static'))


print(os.path.join(os.getcwd(), 'frontend', 'static'))

# DATAFRAMES
df = pd.read_csv("llm_api/us_crop_species_distribution.csv")
df2 = pd.read_csv("llm_api/us_crop_species_distribution2.csv")

df_yield = pd.read_csv('ml_model/yield_data_with_scientific_names.csv')
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'))

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

app.route('/get-plant-yield')
def get_plant_yield():
    crop_scientific_name = 'Zea mays'
    crop_scientific_name = crop_scientific_name.replace(" ","_").lower()
    predicted_yield = get_yield_for_crop_and_country(df_yield, "India", crop_scientific_name)
    lower_price,upper_price = get_yield_lower_upper_price(predicted_yield,crop_scientific_name,2)
    print(lower_price,upper_price)
    return render_template('price-display.html', predicted_yield=predicted_yield, lower_price=lower_price, upper_price=upper_price)

# @app.route('/start_task')
# def start_task():
#     thread = threading.Thread(target=generate_data)
#     thread.start()
#     return jsonify({'status': 'Task started'})

@app.route('/loading-screen')
def loading_screen():
    return render_template('loading-sceen.html')

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


if __name__ == "__main__":
    app.run(debug=True)

