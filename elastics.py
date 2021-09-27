from elasticsearch import Elasticsearch
import json

es = Elasticsearch('http://34.71.96.154:9200')

def insert(jsonD):
	res = es.index(index='chemical', doc_type='doc', body=jsonD)
	return res

def retrieve(body):
	# body = {}
	# body["query"] = {"match":{"title":title}}
	res = es.search(index="chemical",body = body)
	return res

def update(_id,jsonD):
	es.update(index='courses', doc_type="doc", id=_id, body=jsonD)


def delete_by_ids(index,doc_type ,ids):
	bulk = ""
	bulk = bulk + '{ "delete" : { "_index" : "' + index + '", "_type" : "' + doc_type + '", "_id" : "' + ids + '" } }\n'
	res = es.bulk( body=bulk )
	return res



# jsonD = json.load(open("data.json"))

# print (retrieve("Regression"))
# print (delete_by_ids("courses","doc","AW-aZGzD2VPhVUfNDLk-"))
body = {"from":0,"size":100}
# body["query"] = {"match_all":{}}
# print (retrieve(body))

