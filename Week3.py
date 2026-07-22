
import pandas as pd 
import os 

datafolder = "/Users/yanxif/Documents/IDX/summer analyst"

listings = pd.read_csv(os.path.join(datafolder, "listings_filtered.csv"))
sold = pd.read_csv(os.path.join(datafolder, "sold_filtered.csv"))

# step 1 : get the mortgage rate data from FRED

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

# step 2 :resample weekly rates to monthly averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()

# step 3 :  Create a matching year_month key on the MLS datasets

# Sold: key off CloseDate (
sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")

# Listings: key off ListingContractDate 
listings["year_month"] = pd.to_datetime(listings["ListingContractDate"]).dt.to_period("M")

# step 4 : merge

sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(mortgage_monthly, on="year_month", how="left")

# Step 5 : Validate the merge
print("Null rates in sold:", sold_with_rates["rate_30yr_fixed"].isnull().sum())
print("Null rates in listings:", listings_with_rates["rate_30yr_fixed"].isnull().sum())
#make sure the null rate is 0 in both listing and sold


# step 6 :save CSV
sold_with_rates.to_csv(os.path.join(datafolder, "sold_enriched.csv"), index=False)
listings_with_rates.to_csv(os.path.join(datafolder, "listings_enriched.csv"), index=False)