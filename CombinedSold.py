"""
This python script merges all monthly CRMLS_Sold CSV files into one combined
sold.csv, where filters to PropertyType == 'Residential'.
"""

import pandas as pd
import os

datafolder = "/Users/yanxif/Documents/IDX/summer analyst"
filterlist = []

for filename in sorted(os.listdir(datafolder)):
    if filename.startswith("CRMLSSold") and filename.endswith("csv"):
        filepath = os.path.join(datafolder, filename)
        
        if filename == "CRMLSSold202605.csv" :
            df = pd.read_csv(filepath, encoding = "cp1252")
        else:
            df = pd.read_csv(filepath, encoding = "utf-8")
            
        residential_filtered = df[df["PropertyType"] == "Residential"]
        filterlist.append(residential_filtered)

solds = pd.concat(filterlist, ignore_index=True)
solds.to_csv(os.path.join(datafolder, "combined_sold.csv"), index = False)