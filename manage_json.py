import json

def ResetJson():
	jsonqueue=GetJson()
	jsonqueue["Estado Dinamico"]=jsonest=jsonqueue["Estado Estable"]
	return WriteJson(jsonqueue)

def GetJson(hostname):
	try:
		with open('/var/www/FailOverQoSDevNet/JsonFiles/'+hostname+'.json') as json_file:
			data = json.load(json_file)
		return data
	except:
		return 0

def WriteJson(jsonqueue,hostname):
	with open('/var/www/FailOverQoSDevNet/JsonFiles/'+hostname+'.json', 'w') as outfile:
		json.dump(jsonqueue, outfile)
	return 200
	
def AddQueue(nom_queue,valest,vallim,hostname):
	jsonqueue=GetJson(hostname)
	jsonest=jsonqueue["Estado Estable"]
	jsonest[nom_queue]=valest
	jsondin=jsonqueue["Estado Dinamico"]
	jsondin[nom_queue]=valest
	jsonlim=jsonqueue["Estado Limite"]
	jsonlim[nom_queue]=vallim
	jsonqueue["Estado Estable"]=jsonest
	jsonqueue["Estado Dinamico"]=jsondin
	jsonqueue["Estado Limite"]=jsonlim
	return WriteJson(jsonqueue,hostname)
		
def DelQueue(nom_queue,hostname):
	jsonqueue=GetJson(hostname)
	for estado in jsonqueue:
		print(estado)
		jsonqueue[estado].pop(nom_queue,None)
	return WriteJson(jsonqueue,hostname)