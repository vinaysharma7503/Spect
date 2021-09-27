import requests
import json
from elastics import insert

import string 
import random 
  
# initializing size of string  
N = 7
  
# using random.choices() 
# generating random strings  


# url = "http://www.glrinnovations.com/GLRWebservices/api/InVoice/GettingAllGLRProductDetailsCharacter?Char=A"

# data = requests.get(url).json()

# listD = data.get("GLRProductDetailsList")
listC = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


count = 0
for char in listC:
	url = "http://www.glrinnovations.com/GLRWebservices/api/InVoice/GettingAllGLRProductDetailsCharacter?Char={}".format(char)
	data = requests.get(url).json()
	listD = data.get("GLRProductDetailsList")
	count = 0
	for dataD in listD:
		for i in range(1,6):
			keyname = "Price"+str(i)
			p = dataD.get(keyname)
			try:
				if p != "":
					p =str(float(p)*1.3)
			except:
					print (p,"ignored")
		res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N)) 
		cno = "SPT-"+res+"GL"
		dataD["Catalog_No"] = cno
		dataD[keyname] = p
		dataD["char"] = char
		print (count)
		dataD["char"] = char
		dataD["tags"] = [dataD.get("ChemicalName").lower(),dataD.get("Cas").lower()]
		insert(dataD)
		print (count,char)
		#print (dataD)
		count +=1

