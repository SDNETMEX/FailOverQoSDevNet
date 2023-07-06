import sys
from requests.auth import HTTPBasicAuth
import json
import simplejson
import requests
from notificacion_correo import send_email
from qos_wflow import DeviceAlarm
from fo_wflow import Interface_Alarm
from manage_mail_logs import write_mail_logs


def Alarm_Recieved():
	raw_alarm = []
	with open(sys.argv[1],'r') as file:
		raw_alarm = json.load(file)
	alarm=raw_alarm["push.push-change-update"]["push.update-data"]["alm.alarm"]
	try:
		if alarm["alm.perceived-severity"]=="cleared":
			return 200
	except Exception as err:
		print(err)
		return 400
	desc = alarm["alm.description"]
	print(desc)
	if "PowerAlarm" in desc:
		hostname=alarm["alm.node-ref"].split(":")[1]
		interface=alarm["alm.business-key"].split(":")[-1].split("##")[0]
		print(hostname + " " + interface + " Power Alarm")
		write_mail_logs(["Potencia",hostname,interface,"Notificacion"])
		prueba_correo_status = send_email("Notificacion Potencia, Soporte","La Interface: " + interface + " del dispositivo: " + hostname + " supero el umbral de dB permitido, descripcion completa: \n " + desc + " \n\n Atte. Cisco NSO","soporte")
	elif "QoSAlarm" in desc:
		hostname=alarm["alm.node-ref"].split(":")[1]
		queue=alarm["alm.description"].split(";")[-2].split(":")[-1].strip()
		print(hostname + " " + queue)
		if queue != "class-default":
		#	prueba_correo_status = send_email("Notificacion QoS, Operacion","La Queue: " + queue + " del dispositivo: " + hostname + " esta presentando drops, descripcion completa: \n " + desc + " \n\n Atte. Cisco NSO","operacion")
			DeviceAlarm(hostname, queue, desc)
	elif "FOIntAlarm" in desc:
		hostname=alarm["alm.node-ref"].split(":")[1]
		cause_object=alarm["alm.source-object-name"]
		print(hostname + " " + cause_object)
		if "Bundle" not in cause_object:
		#prueba_correo_status = send_email("Notificacion Fail Over, Operacion","La Interface: " + cause_object + " del dispositivo: " + hostname + " esta presentando errores/discards, descripcion completa: \n " + desc + " \n\n Atte. Cisco NSO","operacion")
			Interface_Alarm(hostname, cause_object, desc)
	return 200

print(Alarm_Recieved())
