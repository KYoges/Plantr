import pandas as pd
import glob

# Define the file paths or use a pattern to match all CSV files
data_files = [
    "us_crop_species_distribution.csv",
    "us_crop_species_distribution2.csv",
    "important_crop_distrub_usin.csv"
]

# Initialize an empty list to store dataframes
dataframes = []

# Loop through each file and read it into a dataframe
for file in data_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv("combined_crop_distribution.csv", index=False)

# Load the combined CSV as a DataFrame and display it
print("Combined DataFrame Loaded Successfully!")
print(combined_df.head())
