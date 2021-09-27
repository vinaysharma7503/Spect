import requests
import json
from elastics import insert
import pandas as pd
import string 
import random 
  
# initializing size of string  
N = 7


df = pd.read_csv("Tobeadded.csv")

uniqueC = df["CAS"].unique()

for c in uniqueC:
	dfTemp = df[df["CAS"] == c]
	dfTemp = dfTemp.reset_index(drop=True)
	jsonD = {}
	jsonD["Cas"] = c
	res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N)) 
	jsonD["ChemicalName"] = dfTemp["Item"][0]
	jsonD["Catalog_No"] = "SPT-"+res+df["tag"][0]
	dfTemp.reset_index(drop=True,inplace=True)
	jsonD["char"] = df["char"][0]
	jsonD["tags"] = [jsonD.get("ChemicalName").lower(),jsonD.get("Cas").lower()]
	for i in range(0,len(dfTemp)):
		keynameP = "Price"+str(i+1)
		packP = "Pack"+str(i+1)
		jsonD[keynameP] = str(dfTemp["Cost"][i])
		jsonD[packP] = dfTemp["Pack"][i]
	jsonD["Price6"] = ""
	jsonD["Pack6"] = ""
	insert(jsonD)



