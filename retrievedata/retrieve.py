from elasticsearch import Elasticsearch
import json
import pandas as pd
import os
es = Elasticsearch('http://34.71.96.154:9200')


def retrieve(body):
	# body = {}
	# body["query"] = {"match":{"title":title}}
	res = es.search(index="chemical",body = body)
	return res



def main():
	count = 0
	start = 0
	body = {"from":start,"size":2000}
	res = retrieve(body)
	dataL = res.get("hits").get("hits")
	while(len(dataL)!=0):
		df = pd.DataFrame()
		print(len(dataL))
		for d in dataL:
			mainD = d.get("_source")
			for keys in mainD:
				df.loc[count,keys] = str(mainD.get(keys,""))
			count += 1
			print(count)
		df.to_csv("backup{}.csv".format(str(start)))
		count = 0
		start += 2000
		body = {"from":start,"size":2000}
		res = retrieve(body)
		dataL = res.get("hits").get("hits")

	# df.to_csv("backup{}.csv".format(str(start)))

main()