from geopy.geocoders import Nominatim
from flask import Flask, request, flash, jsonify


# need to convert the address the user has inputted into longitude and latitude
def get_location(postcode):
    geoLocator = Nominatim(user_agent = "cropPrediction")
    location = geoLocator.geocode(postcode + ", USA")

    if location:
        return location.latitude, location.longitude
    return None, None

# features are already being given
# need to present a list of the best crops
# the user then selects the best crop - this choice is then passed to the llm tool

def predict_crop(postcode):
    lat, lon = get_location(postcode)

    if lat is None or lon is None:
        return {"error: Invalid postcode or geolocation has failed"}
    
    return get_best_crops(lat, lon)

# need to let the user pass in a choice through the front-end
def user_choice(postcode, choice):
    crops = predict_crop(postcode)

    if "error" in crops:
        return crops
    
    if choice not in crops:
        return {"Invalid choice"}
    
    llm_response = query_llm(choice)
    
    return  jsonify({"llm_response": llm_response})

# viraj and demir's method
def get_best_crops():
    pass