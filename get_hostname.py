#!/usr/bin/python3
from netmiko import ConnectHandler
from manage_json import GetJson, WriteJson
import os

username = os.environ['username_ssh']
password = os.environ['password_ssh']

def get_hostname(ip):
	try:
		hosts=GetJson("Known_Hosts")
		for host in hosts:
			if host == ip:
				return hosts[ip]
	except Exception as err:
		pass
	try:
		credenciales = {
			"host": ip,
			"username": username,
			"password": password,
			"port": 22,
			"global_delay_factor": 4,
			"device_type": "cisco_xr"
		} 

		with ConnectHandler(**credenciales) as m:
			result = m.send_command_timing("show run | inc hostname")
		m.disconnect()
		hostname=result.split('hostnameprefix')[1]
		if hosts==0:
			WriteJson({ip:hostname.strip()},"Known_Hosts")
		else:
			hosts[ip]=hostname.strip()
			WriteJson(hosts,"Known_Hosts")

		return hostname.strip()

	except Exception as err:
		print (str(err) + ip)
		pass