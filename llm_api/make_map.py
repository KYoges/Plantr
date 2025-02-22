import folium
import pandas as pd

# Load the CSV file (Update the filename accordingly)
csv_file = "Arabidopsis thaliana_us_distribution.csv"  # Change this to your actual file
df = pd.read_csv(csv_file)

# Ensure only valid latitude/longitude values are used
df = df.dropna(subset=["latitude", "longitude"])
df["year"] = df["year"].fillna(0)
# Create a folium map centered at the average location
map_center = [df["latitude"].mean(), df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=4)

# Add plant occurrence markers
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['scientificName']} ({row['country']}, {int(row['year'])})",
        icon=folium.Icon(color="green")
    ).add_to(m)

# Save the map as an HTML file
m.save("plant_distribution_map.html")
print("Map saved! Open 'plant_distribution_map.html' in your browser to view.")

