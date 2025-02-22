import requests
import pandas as pd
import time
crop_families = [
    "Poaceae"
   # , "Fabaceae", "Brassicaceae", "Solanaceae", 
   # "Asteraceae", "Rosaceae", "Cucurbitaceae"
]

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

def get_all_plants():
    
    base_url = "https://api.gbif.org/v1/species/search"
    limit = 1000  
    offset = 0  
    all_plants = []  
    
    while True:
        print(f"Fetching records {offset} - {offset + limit}...")
        response = requests.get(f"{base_url}?kingdom=Plantae&limit={limit}&offset={offset}")
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        data = response.json()
        results = data.get("results", [])
    
        if not results:
            break
        
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

        offset += limit
        time.sleep(1)

    # Convert to DataFrame
    df = pd.DataFrame(all_plants)
    
    # Save to CSV
    df.to_csv("gbif_plantae_species.csv", index=False)
    print(f"Saved {len(df)} plant records to gbif_plantae_species.csv")

def get_all_plants_distribution_us():
    """Fetches all plant location data from GBIF for the United States"""
    
    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000  # Max per request
    offset = 0  # Pagination start
    all_locations = []  # Store plant occurrence data
    
    while True:
        print(f"Fetching records {offset} - {offset + limit} for plants in the US...")

        # GBIF API request with filters for US occurrences
        response = requests.get(
            f"{base_url}?kingdom=Plantae&country=US&limit={limit}&offset={offset}"
        )
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        data = response.json()
        results = data.get("results", [])
        
        # Stop if no more results
        if not results:
            break

        # Extract relevant fields
        for record in results:
            if "decimalLatitude" in record and "decimalLongitude" in record:
                all_locations.append({
                    "scientificName": record.get("scientificName"),
                    "latitude": record.get("decimalLatitude"),
                    "longitude": record.get("decimalLongitude"),
                    "country": record.get("country"),
                    "year": record.get("year"),
                    "month": record.get("month"),
                    "day": record.get("day"),
                })

        # Move to the next batch
        offset += limit
        
        # Avoid API rate limits
        time.sleep(1)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_locations)
    df.to_csv("all_plants_us_distribution.csv", index=False)
    
    print(f"✅ Saved {len(df)} plant records from the US to all_plants_us_distribution.csv.")
    return df


def get_crop_distribution_us(family_list):
    """Fetches agricultural crop locations in the US from GBIF"""
    
    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000  # Maximum per request
    offset = 0  # Pagination start
    all_locations = []  # Store crop occurrences

    for family in family_list:
        print(f"Fetching crop family: {family}...")

        offset = 0  # Reset offset for each family
        while True:
            print(f"Fetching records {offset} - {offset + limit} for {family} in the US...")

            # GBIF API request for the family, filtering by US location
            response = requests.get(
                f"{base_url}?family={family}&country=US&limit={limit}&offset={offset}"
            )
            
            if response.status_code != 200:
                print(f"Error fetching data for {family}: {response.status_code}")
                break
            
            data = response.json()
            results = data.get("results", [])
            
            # If no more results, stop pagination
            if not results:
                break

            # Extract relevant fields
            for record in results:
                if "decimalLatitude" in record and "decimalLongitude" in record:
                    all_locations.append({
                        "scientificName": record.get("scientificName"),
                        "family": family,
                        "latitude": record.get("decimalLatitude"),
                        "longitude": record.get("decimalLongitude"),
                        "country": record.get("country"),
                        "year": record.get("year"),
                        "month": record.get("month"),
                        "day": record.get("day"),
                    })

            # Move to the next batch
            offset += limit
            
            # Prevent rate limiting
            time.sleep(1)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_locations)
    df.to_csv("us_agricultural_crops.csv", index=False)
    
    print(f"✅ Saved {len(df)} agricultural crop records to us_agricultural_crops.csv.")
    return df



def get_crop_families_distribution_us(family_list):
    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000  # Max per request
    all_family_locations = []  # Store family occurrences

    for family in family_list:
        print(f"Fetching data for crop family: {family}...")

        offset = 0  # Reset offset for each family
        while True:
            print(f"Fetching records {offset} - {offset + limit} for {family} in the US...")

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
                    all_family_locations.append({
                        "family": family,
                        "latitude": record.get("decimalLatitude"),
                        "longitude": record.get("decimalLongitude"),
                        "country": record.get("country"),
                        "year": record.get("year"),
                        "month": record.get("month"),
                        "day": record.get("day"),
                    })

            offset += limit
            time.sleep(1)

    # Save data to CSV
    df_families = pd.DataFrame(all_family_locations)
    df_families.to_csv("us_crop_families_distribution.csv", index=False)
    
    print(f"✅ Saved {len(df_families)} crop family records to us_crop_families_distribution.csv.")
    return df_families

def get_crop_species_distribution_us(family_list):
    """Fetches all agricultural crop species in the US from GBIF"""

    base_url = "https://api.gbif.org/v1/occurrence/search"
    limit = 1000
    all_species_locations = []

    for family in family_list:
        print(f"Fetching species for crop family: {family}...")

        offset = 0  
        while True:
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

            offset += limit
            time.sleep(2)

    # Save data to CSV
    df_species = pd.DataFrame(all_species_locations)
    df_species.to_csv("us_crop_species_distribution.csv", index=False)
    
    print(f"✅ Saved {len(df_species)} crop species records to us_crop_species_distribution.csv.")
    return df_species

get_crop_families_distribution_us(crop_families)



