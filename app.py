from flask import Flask, render_template, jsonify, request, redirect, url_for
from crop import predict_crop, user_choice
import threading
import time
import os

# Initialize Flask app with the correct template folder
app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'),
            static_folder=os.path.join(os.getcwd(), 'frontend', 'static'))
import pandas as pd
from price_pred_api.get_yield import *
import json
#get_yield_for_crop_and_country(yield_df, country, crop_scientific_name)
df_yield = pd.read_csv('ml_model/yield_data_with_scientific_names.csv')
print(df_yield)
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'))

# This prints the current working directory to confirm we're using the right path
print("Current working directory:", os.getcwd())

def generate_data():
    time.sleep(5)

@app.route('/')
def index():
    return render_template('loading-sreen.html')  

    return render_template('loading-sreen.html')  # Rendering the template
@app.route('/get-plant-yield')
def get_plant_yield():
    crop_scientific_name = 'Zea mays'
    crop_scientific_name = crop_scientific_name.replace(" ","_").lower()
    predicted_yield = get_yield_for_crop_and_country(df_yield, "India", crop_scientific_name)
    lower_price,upper_price = get_yield_lower_upper_price(predicted_yield,crop_scientific_name,2)
    print(lower_price,upper_price)
    return render_template('price-display.html', predicted_yield=predicted_yield, lower_price=lower_price, upper_price=upper_price)
@app.route('/start_task')
def start_task():
    # Start the background task in a separate thread
    thread = threading.Thread(target=generate_data)
    thread.start()
    return jsonify({'status': 'Task started'})

@app.route('/redirect_after_delay')
def redirect_after_delay():
    # Simulate a 2-second delay
    time.sleep(2)
    # After the delay, redirect to index.html (or the desired route)
    return redirect(url_for('main_page'))

@app.route('/main_page')
def main_page():
    # Render the main page after the delay
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

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

