import pandas as pd 
import os 


datafolder = "/Users/yanxif/Documents/IDX/summer analyst"

listings = pd.read_csv(os.path.join(datafolder, "combined_listing.csv"))
sold = pd.read_csv(os.path.join(datafolder, "combined_sold.csv"))


print("listings")
print("Shape (rows, columns):", listings.shape)
print("Column names:", listings.columns.tolist())
print("                  ")
print("sold")
print("Shape (rows, columns):", sold.shape)
print("Column names:", sold.columns.tolist())


#There are some columns that are duplicates in the combined_listing csv,
#for example :  "PropertyType" and "PropertyType.1", 
#          "ListAgentFirstName" and "ListAgentFirstName.1"
# I found out that the information inside the columns are exactly the same
#To fix this, I just made a list of all the columns that has .1 dupes and have them removed
dupes = []
for i in listings.columns:
    if i.endswith(".1"):
        dupes.append(i)
        
listings = listings.drop(columns=dupes)

#This prints out the data type of every column in both datasets
#Doing this makes sure everything lines up, exp ClosePrice is float64, AgentName is str
print("\nListings dtypes:")
for col in listings.columns:
    print(col, "->", listings[col].dtype)

print("\nSold dtypes:")
for col in sold.columns:
    print(col, "->", sold[col].dtype)
#Through this, I determined that everything looks good 



#Flagging columns that are over 90% null 

print("\nMissing Value : listings")
listings_missing = listings.isnull().sum() 
#.isnull turns dataframe into true/false, the .sum() counts the amount of true(which is null)
listings_missing_pct = (listings_missing / len(listings)) * 100

for i in listings.columns:
    print(i, "->", listings_missing[i], "missing, or = to",
          round(listings_missing_pct[i], 2), "% missing.") 

#Reads the columns that have over 90% in listing
print("\nColumns over 90% missing in listings are :")
listings_flagged = listings_missing_pct[listings_missing_pct > 90]
for i in listings_flagged.index:
    print(i, "->", round(listings_flagged[i], 2), "%")
    

print("\nMissing Value : sold")
sold_missing = sold.isnull().sum()
sold_missing_pct = (sold_missing / len(sold)) * 100

for i in sold.columns:
    print(i, "->", sold_missing[i], "missing, or = to",
          round(sold_missing_pct[i], 2), "% missing.")

#Reads the columns that have over 90% in sold
print("\nColumns over 90% missing in sold:")
sold_flagged = sold_missing_pct[sold_missing_pct > 90]
for i in sold_flagged.index:
    print(i, "->", round(sold_flagged[i], 2), "%")

#Drops all listing/sold columns that have over 90% null
listings = listings.drop(columns=listings_flagged.index)
sold = sold.drop(columns=sold_flagged.index)

#Numeric Distribution Summmary of Min, Max, Mean, Median, and Percentiles
#for ClosePrice, Living Area, and DaysOnMarket

numeric_fields = ["ClosePrice", "LivingArea", "DaysOnMarket"]

print("\n Numeric Distribution: listings ")
for col in numeric_fields:
    print("\n--", col, "")
    print(listings[col].describe())

print("\n Numeric Distribution: sold ")
for col in numeric_fields:
    print("\n--", col, "")
    print(sold[col].describe())
    
#save the datasets as new CSV

listings.to_csv(os.path.join(datafolder, "listings_filtered.csv"), index=False)
sold.to_csv(os.path.join(datafolder, "sold_filtered.csv"), index=False)

