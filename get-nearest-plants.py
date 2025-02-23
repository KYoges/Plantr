import math

# Haversine formula to compute the distance between two latitude/longitude points
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Function to find the k nearest plant records based on user's coordinates
def find_nearest_plants(user_lat, user_lon, plant_records, k=3):
    # Create a list of tuples (record, distance)
    distances = []
    for record in plant_records:
        distance = haversine_distance(user_lat, user_lon, record['latitude'], record['longitude'])
        distances.append((record, distance))
    
    # Sort the list by distance (ascending)
    distances.sort(key=lambda x: x[1])
    
    # Return the top k nearest records; if there are fewer than k records, return all
    return distances[:min(k, len(distances))]

# Example plant records (this could come from your CSV data)
plant_records = [
    {
        'scientificName': 'Manihot esculenta Crantz',
        'latitude': 27.870916,
        'longitude': -82.262146,
        'country': 'United States of America',
        'year': 2025,
        'month': 1,
        'day': 9
    },
    {
        'scientificName': 'Manihot esculenta Crantz',
        'latitude': 19.724346,
        'longitude': -155.138781,
        'country': 'United States of America',
        'year': 2025,
        'month': 1,
        'day': 13
    },
    # Add more plant records as needed...
]

# Suppose the user provides their coordinates
user_lat = 25.0
user_lon = -80.0

# Get three nearest plants as options
nearest_plants = find_nearest_plants(user_lat, user_lon, plant_records, k=3)

# Display the options
for idx, (plant, distance) in enumerate(nearest_plants, start=1):
    print(f"Option {idx}:")
    print(f"  Scientific Name: {plant['scientificName']}")
    print(f"  Location: ({plant['latitude']}, {plant['longitude']})")
    print(f"  Distance: {distance:.2f} km")
    print()

