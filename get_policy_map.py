import os
import requests

ip_nso = os.environ['IP_NSO']
port_nso = os.environ['PORT_NSO']
auth = os.environ['AUTH']
def get_policy_map(hostname):

    try:
        url = f"http://{ip_nso}:{port_nso}/api/running/devices/device/"+hostname+"/config/cisco-ios-xr:policy-map/QSP-ALL-CORE-OUT/class/class-ref"
        headers = {'Accept': 'application/vnd.yang.collection+json','Authorization': f'Basic {auth}'}
        response = requests.request("GET", url, headers=headers, data = {})
        queue=response.json()['collection']['tailf-ned-cisco-ios-xr:class-ref']
        json={}
        for q in queue:
            #print(q)
            try:
                json[q['map']]=q['police-rate-unit']['police']['rate']['percent']
            except:
                pass
        return(json)
    except Exception as err:
        print(str(err))
		
#print(get_policy_map("PE_INTERNET_ASR9K10_GDL_CTC"))