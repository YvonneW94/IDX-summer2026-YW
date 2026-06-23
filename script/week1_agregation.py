import pandas as pd
import glob
import os

# Set folder path
data_path = "/Users/wing/IDX intern/csv"

# Get all listing files
listing_files = sorted(glob.glob(os.path.join(data_path, "CRMLSListing*.csv")))

# Get all sold files
sold_files = sorted(glob.glob(os.path.join(data_path, "CRMLSSold*.csv")))

print(f"Listing files found: {len(listing_files)}")
print(f"Sold files found: {len(sold_files)}")

# Read and concatenate
listing_dfs = [pd.read_csv(file) for file in listing_files]
sold_dfs = [pd.read_csv(file) for file in sold_files]

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

# Save outputs
output_path = "outputs"
os.makedirs(output_path, exist_ok=True)

listings_res.to_csv(os.path.join(output_path, "combined_listings_residential.csv"), index=False)
sold_res.to_csv(os.path.join(output_path, "combined_sold_residential.csv"), index=False)

print("Files saved successfully.")