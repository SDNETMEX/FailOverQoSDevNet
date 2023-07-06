from requests.auth import HTTPBasicAuth
import json
import requests
import time
import os

ip_nso = os.environ['IP_NSO']
port_nso = os.environ['PORT_NSO']
auth = os.environ['AUTH_NSO']

def show_interface(hostname, interface):

    for intento in range(0, 3):
        try:
            url = f"http://{ip_nso}:{port_nso}/api/operational/devices/device/"+hostname+"/live-status/cisco-ios-xr-stats:exec/_operations/show"
            headers = {'Content-Type': 'application/vnd.yang.data+json', 'Authorization': f'Basic {auth}'}
            show = {"show": {"args": "run interface " + interface}}
            show_json = json.dumps(show)
            r = requests.request("POST",url, headers=headers,data=show_json)
            print("aqui")
            print(r.text+"-"+str(len(r.text)))
            print("2")
            if len(r.text) < 1 and "." in hostname:
                hostsplit=hostname.split(".")[0]
                print(hostname + " - " + hostsplit)
                return show_interface(hostsplit, interface)
            result = (r.json()["tailf-ned-cisco-ios-xr-stats:output"]["result"]).split("\n")
            print(result)
            new_result = []
            no_bundle=""
            for i in result:
                if "bundle" in i:
                    no_bundle=i.strip().split(" ")[2].strip()
                    print(no_bundle)
            if no_bundle=="":
                return -1
            show = {"show": {"args": "interface Bundle-Ether" + no_bundle}}
            show_json = json.dumps(show)
            r = requests.request("POST",url, headers=headers,data=show_json)
            result = (r.json()["tailf-ned-cisco-ios-xr-stats:output"]["result"]).split("\n")
            print("\n".join(result))
            for i in result:
                if "Active" in i:
                    new_result.append(i.split("        ")[0].strip())
            print("\n".join(new_result))
            if len(new_result)>1:
                return no_bundle
            else:
                return 0

        except Exception as err:
            print(hostname + " " +interface +" --- "+str(err))
            time.sleep(30)
    return 400
