from elastics import retrieve,delete_by_ids
import pandas as pd

df = pd.read_csv("Tobeadded.csv")

for i in range(0,len(df)):
	body = {}
	body["query"] = {"match":{"tags":df["CAS"][i]}}
	data = retrieve(body)
	listD = data.get("hits").get("hits")
	flag = 0
	for jsonD in listD:
		id_ = jsonD.get("_id")
		mainJ = jsonD.get("_source")
		if mainJ['Cas'].strip() == df["CAS"][i].strip():
			flag = 1
			print ("Going to delete",df["CAS"][i].strip())
			delete_by_ids("chemical","doc",id_)
			break
	if flag == 0:
		print ("Was not able to delete ",df["CAS"][i])