import requests
import pandas as pd
import time
import os


df = pd.read_csv('llm_api/important_crops.csv')


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


def get_crop_species_distribution_us(family_list):

    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000
    all_species_locations = []
    csv_filename = "imp_us_crop_species_distribution.csv"     
    if os.path.exists(csv_filename):
        print(f"Loading previous data from {csv_filename}...")
        existing_data = pd.read_csv(csv_filename)
        all_species_locations = existing_data.to_dict(orient="records")
        print(f"Loaded {len(all_species_locations)} previous records.")
    
    for family in family_list:
        print(f"Fetching species for crop family: {family}...")

        offset = 0  
        while True:
            try:
                print(f"Fetching records {offset} - {offset + limit} for species in {family} in the US...")

                response = requests.get(
                    f"{base_url}?family={family}&country=US&limit={limit}&offset={offset}"
                )
                
                if response.status_code != 200:
                    print(f"Error fetching data for {family}: {response.status_code}")
                    break

                data = response.json()
                results = data.get("results", [])

                if not results:
                    break

                for record in results:
                    if "decimalLatitude" in record and "decimalLongitude" in record:
                        all_species_locations.append({
                            "scientificName": record.get("scientificName"),
                            "family": family,
                            "latitude": record.get("decimalLatitude"),
                            "longitude": record.get("decimalLongitude"),
                            "country": record.get("country"),
                            "year": record.get("year"),
                            "month": record.get("month"),
                            "day": record.get("day"),
                        })
                pd.DataFrame(all_species_locations).to_csv(csv_filename, index=False)
                print(f"✅ Saved {len(all_species_locations)} records to {csv_filename}.")
                
                offset += limit
                time.sleep(2)
                
            except Exception as e:
                print(f"An error occurred while fetching data for {family}: {e}")
                break  

    try:
        df_species = pd.DataFrame(all_species_locations)
        df_species.to_csv(csv_filename, index=False)
        print(f"✅ Final save: {len(df_species)} crop species records saved to {csv_filename}.")
    except Exception as e:
        print(f"Error during final save: {e}")
    
    return pd.DataFrame(all_species_locations)


def get_crop_species_distribution_us(species_list):
    """Fetches all agricultural crop species in the US from GBIF and saves progress regularly"""

    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000
    all_species_locations = []
    csv_filename = "us_crop_species_distribution.csv"
    
    # Try to load previously saved data, if any
    if os.path.exists(csv_filename):
        print(f"Loading previous data from {csv_filename}...")
        existing_data = pd.read_csv(csv_filename)
        all_species_locations = existing_data.to_dict(orient="records")
        print(f"Loaded {len(all_species_locations)} previous records.")
    
    for species in species_list:
        print(f"Fetching species: {species}...")

        offset = 0  
        while True:
            try:
                print(f"Fetching records {offset} - {offset + limit} for species {species} in the US...")

                response = requests.get(
                    f"{base_url}?scientificName={species}&country=US&limit={limit}&offset={offset}"
                )
                
                if response.status_code != 200:
                    print(f"Error fetching data for {species}: {response.status_code}")
                    break

                data = response.json()
                results = data.get("results", [])

                if not results:
                    break

                for record in results:
                    if "decimalLatitude" in record and "decimalLongitude" in record:
                        all_species_locations.append({
                            "scientificName": record.get("scientificName"),
                            "latitude": record.get("decimalLatitude"),
                            "longitude": record.get("decimalLongitude"),
                            "country": record.get("country"),
                            "year": record.get("year"),
                            "month": record.get("month"),
                            "day": record.get("day"),
                        })

                # Save progress after each species
                pd.DataFrame(all_species_locations).to_csv(csv_filename, index=False)
                print(f"✅ Saved {len(all_species_locations)} records to {csv_filename}.")
                
                # Move to next batch
                offset += limit
                time.sleep(2)
                
            except Exception as e:
                print(f"An error occurred while fetching data for {species}: {e}")
                break  # Exit the loop if any error occurs

    # Final save to ensure all data is written
    try:
        df_species = pd.DataFrame(all_species_locations)
        df_species.to_csv(csv_filename, index=False)
        print(f"✅ Final save: {len(df_species)} crop species records saved to {csv_filename}.")
    except Exception as e:
        print(f"Error during final save: {e}")
    
    return pd.DataFrame(all_species_locations)

# get_crop_species_distribution_us(df['Scientific Name'].to_numpy())



