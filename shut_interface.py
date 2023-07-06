# -- coding: utf-8 --
from __future__ import print_function
import requests
import re
import os

ip_nso = os.environ['IP_NSO']
port_nso = os.environ['PORT_NSO']
auth = os.environ['AUTH_NSO']

HEADERS = {'content-type': 'application/vnd.yang.data+xml', 'Accept': 'application/vnd.yang.data+json', 'Authorization': f'Basic {auth}'}

def shut_interface(device, interface):
    typeint=re.findall("[a-zA-Z]",interface)
    inter=''.join(typeint)
    id_int=interface.replace(inter,"")
    print(device)
    print(inter + " - " + id_int)
    data = '<devices xmlns="http://tail-f.com/ns/ncs">' \
           '<device>' \
           '<name>'+device+'</name>' \
           '<config>' \
           '<interface xmlns="http://tail-f.com/ned/cisco-ios-xr">' \
           '<'+inter+'>' \
           '<id>'+id_int+'</id>' \
           '<shutdown/>' \
           '</'+inter+'>' \
           '</interface>' \
           '</config>' \
           '</device>' \
           '</devices>'

    try:
#        r = requests.request("PATCH",'http://'+ip_nso+':8080/api/running/', data=data, headers=HEADERS, verify=False)
        r = requests.request("PATCH",f'http://{ip_nso}:{port_nso}/api/running?dryrun=native', data=data, headers=HEADERS, verify=False)
        if "Either address" in r.text and "." in device:
            hostsplit=device.split(".")[0]
            print(device + " - " + hostsplit)
            return shut_interface(hostsplit, interface)
        print('Asi quedaria la nueva config: ')
        print(r.text)
        return (r.text).split("<data>")[1].split("</data>")[0]
    except Exception as err:
        print(err)
        print("Hubo algun problema")
        return 400
