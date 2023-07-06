import requests
import os

auth = os.environ['AUTH_NSO']
ip_nso = os.environ['IP_NSO']
HEADERS = {'content-type': 'application/vnd.yang.data+xml', 'Accept': 'application/vnd.yang.data+json', 'Authorization': f'Basic {auth}'}


def elevar_porcentaje(hostname,cola,porcentaje):

    data = '<devices xmlns="http://tail-f.com/ns/ncs">' \
			  '<device>' \
				'<name>'+hostname+'</name>' \
				  '<config>' \
				  '<policy-map xmlns="http://tail-f.com/ned/cisco-ios-xr">' \
					'<name>QSP-ALL-CORE-OUT</name>' \
					'<class>' \
					  '<class-ref>' \
						'<map>'+cola+'</map>' \
						'<police-rate-unit>' \
						  '<police>' \
							'<rate>' \
							  '<percent>'+porcentaje+'</percent>' \
							'</rate>' \
						  '</police>' \
						'</police-rate-unit>' \
					  '</class-ref>' \
					'</class>' \
				  '</policy-map>' \
				  '</config>' \
			  '</device>' \
			'</devices>'

    r1 = requests.request("PATCH",'http://'+ip_nso+':8080/api/running/?dryrun=native', data=data, headers=HEADERS, verify=False)
    if "Either address" in r1.text and "." in hostname:
        hostsplit=hostname.split(".")[0]
        print(hostname + " - " + hostsplit)
        return elevar_porcentaje(hostsplit,cola,porcentaje)
    if r1.status_code < 300:
        print (r1.status_code)
        return ((r1.text).split("<data>")[1].split("</data>")[0])


    else:
        print(r1.text)
        return 400

