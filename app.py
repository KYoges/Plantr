from flask import Flask, render_template, jsonify
import threading
import time
import os
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
    time.sleep(5)  # Simulating a time-consuming task
    # Place your actual data generation code here.

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)

