#!/usr/bin/python3
from manage_json import GetJson, WriteJson
from datetime import datetime
from get_policy_map import get_policy_map
from main_services import Get_Devices

def rollback_cron():
	devices = Get_Devices()
	for hostname in devices:
		json_val=get_policy_map(hostname)
		json_host=GetJson(hostname)
		json_logs=GetJson("Logs")
		json_max_val=GetJson("max_values")
		for queue in json_host[hostname]:
			success=1
			if json_host[hostname][queue]>0:
				try:
					porcentaje_avance=str(json_val[queue]+json_host[hostname][queue]) + " - " + str(json_val[queue])
					fecha=str(datetime.now())
					print(fecha)
					json_logs[fecha]=[hostname,queue,porcentaje_avance]
					json_host[hostname][queue]=0
					WriteJson(json_host,hostname)
					WriteJson(json_logs,"Logs")
				except:
					success=0
					break
		if success==0:
			print(json_host["intentos"])
			json_host["intentos"]+=1
		else:
			print(json_host["intentos"])
			json_host["intentos"]=0
		WriteJson(json_host,hostname)
		print("El dispositivo: " + hostname + " ha sufrido un Rollback ,  \n\n Atte. Cisco NSO")
	return "Rollback Completado"

print(rollback_cron())
