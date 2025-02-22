import requests
import pandas as pd

def get_plant_info(plant_name):
    url = f"https://api.gbif.org/v1/species/search?q={plant_name}&kingdom=Plantae"
    response = requests.get(url)
    data = response.json()
    species_list = []
    for result in data["results"]:
        species_list.append({
            "taxonID": result.get("key"),
            "scientificName": result.get("scientificName"),
            "canonicalName": result.get("canonicalName"),
            "kingdom": result.get("kingdom"),
            "phylum": result.get("phylum"),
            "class": result.get("class"),
            "order": result.get("order"),
            "family": result.get("family"),
            "genus": result.get("genus"),
            "species": result.get("species"),
            "rank": result.get("rank"),
            "status": result.get("taxonomicStatus")
        })
    
    return species_list

import requests
import pandas as pd
import time

def get_all_plants():
    
    base_url = "https://api.gbif.org/v1/species/search"
    limit = 1000  # Max limit per request
    offset = 0  # Pagination start
    all_plants = []  # List to store results
    
    while True:
        print(f"Fetching records {offset} - {offset + limit}...")

        # API request with pagination
        response = requests.get(f"{base_url}?kingdom=Plantae&limit={limit}&offset={offset}")
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        data = response.json()
        results = data.get("results", [])
        
        # If no more results, stop pagination
        if not results:
            break
        
        # Extract relevant fields
        for result in results:
            all_plants.append({
                "taxonID": result.get("key"),
                "scientificName": result.get("scientificName"),
                "kingdom": result.get("kingdom"),
                "phylum": result.get("phylum"),
                "class": result.get("class"),
                "order": result.get("order"),
                "family": result.get("family"),
                "genus": result.get("genus"),
                "species": result.get("species"),
                "rank": result.get("rank"),
                "status": result.get("taxonomicStatus")
            })

        # Move to the next page
        offset += limit
        
        # Delay to avoid rate-limiting
        time.sleep(1)

    # Convert to DataFrame
    df = pd.DataFrame(all_plants)
    
    # Save to CSV
    df.to_csv("gbif_plantae_species.csv", index=False)
    print(f"Saved {len(df)} plant records to gbif_plantae_species.csv")

get_all_plants()

