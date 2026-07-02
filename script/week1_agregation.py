import pandas as pd
import glob  #Import glob to find multiple files that match a filename pattern.
import os #Import os to work with file paths and folders.

# Set folder path
data_path = "/Users/wing/IDX intern/csv"

# Get all listing files
listing_files = sorted(glob.glob(os.path.join(data_path, "CRMLSListing*.csv")))

# Get all sold files
sold_files = sorted(glob.glob(os.path.join(data_path, "CRMLSSold*.csv")))

print(f"Listing files found: {len(listing_files)}")
print(f"Sold files found: {len(sold_files)}")

# Read and concatenate
listing_dfs = []

for file in listing_files:
    df = pd.read_csv(file, low_memory=False)

    # If file name contains "_filled", remove the last two extra columns
    if "_filled" in file:
        df = df.iloc[:, :-2]

    listing_dfs.append(df)


sold_dfs = []

for file in sold_files:
    df = pd.read_csv(file, low_memory=False)

    # If file name contains "_filled", remove the last two extra columns
    if "_filled" in file:
        df = df.iloc[:, :-2]

    sold_dfs.append(df)

listings = pd.concat(listing_dfs, ignore_index=True)
sold = pd.concat(sold_dfs, ignore_index=True)

# Row counts before filter
print("Before Residential filter:")
print("Listings:", listings.shape)
print("Sold:", sold.shape)

# Filter Residential
listings_res = listings[listings["PropertyType"] == "Residential"]
sold_res = sold[sold["PropertyType"] == "Residential"]

# Row counts after filter
print("After Residential filter:")
print("Listings:", listings_res.shape)
print("Sold:", sold_res.shape)

# --------------------------------------------------
# Week 1: Monthly Dataset Aggregation
# IDX Exchange Internship
# --------------------------------------------------

# Files loaded:
# Listing files found: 29
# Sold files found: 29

# Before Residential filter:
# Listings dataset shape: (930311, 84)
# Sold dataset shape: (643229, 84)

# After Residential filter:
# Residential Listings dataset shape: (591980, 84)
# Residential Sold dataset shape: (433158, 84)

# Save outputs
output_path = "outputs"
os.makedirs(output_path, exist_ok=True)

listings_res.to_csv(os.path.join(output_path, "combined_listings_residential.csv"), index=False)
sold_res.to_csv(os.path.join(output_path, "combined_sold_residential.csv"), index=False)

print("Files saved successfully.")