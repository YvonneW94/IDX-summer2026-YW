# IDX Exchange MLS Analytics Internship

## Week 1: Monthly Dataset Aggregation

This week focuses on combining monthly MLS listing and sold transaction CSV files into two master datasets for later analysis.

## Objectives

- Load all monthly `CRMLSListing` files.
- Load all monthly `CRMLSSold` files.
- Concatenate monthly files into combined listing and sold datasets.
- Filter both datasets to `PropertyType == "Residential"`.
- Export the residential-only datasets as new CSV files.

## Files Processed

- Listing files found: 29
- Sold files found: 29

## Row Counts

### Before Residential Filter

- Listings: 930,311 rows, 84 columns
- Sold: 643,229 rows, 82 columns

### After Residential Filter

- Listings: 616,048 rows, 84 columns
- Sold: 450,699 rows, 84 columns

## Outputs

The script generates:

- `combined_listings_residential.csv`
- `combined_sold_residential.csv`

Output CSV files are not uploaded to GitHub because they are large and contain confidential MLS data.

## Tools Used

- Python
- Pandas
- glob
- os

## Notes

Some columns produced mixed-type warnings during import. These warnings do not stop the aggregation process, but they will be reviewed in the data validation stage.
