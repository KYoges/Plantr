import folium
import pandas as pd

csv_file = "Arabidopsis thaliana_us_distribution.csv"  
df = pd.read_csv(csv_file)

df = df.dropna(subset=["latitude", "longitude"])
df["year"] = df["year"].fillna(0)
map_center = [df["latitude"].mean(), df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=4)

for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['scientificName']} ({row['country']}, {int(row['year'])})",
        icon=folium.Icon(color="green")
    ).add_to(m)

m.save("plant_distribution_map.html")
print("Map saved! Open 'plant_distribution_map.html' in your browser to view.")

