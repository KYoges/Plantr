from flask import Flask, request, flash, jsonify
from crop import predict_crop, user_choice

app = Flask(__name__)

@app.route('/predict', methods = ['GET'])
def predict():
    # using weather and other forecasts of that specific region to predict the crop to grow for that region
    location = request.args.get('location')

    if not location:
        flash("Missing location. Please provide a location to check")

    crops = predict_crop(location)
    return jsonify({"recommended_crops": crops})  

@app.route('/choose', methods = ['POST'])
def choose():
    data = request.get_json()
    location = data.get("location")
    choice = data.get("choice")

    if not location or not choice:
        return jsonify({"error": "Invalid location or choice"}), 400

    return jsonify(user_choice(location, choice))
    


    


