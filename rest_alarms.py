# -- coding: utf-8 --
from __future__ import print_function
from ws4py.client.threadedclient import WebSocketClient
from subprocess import call
import os
import base64
from info_logs import info_logs
import ssl

ip_epn = os.environ['IP_EPN']
username = os.environ['username']
password = os.environ['password']
auth = os.environ['AUTH_EPN']
cookie = os.environ['COOKIE']

HEADERS5 = {'content-type': 'application/vnd.yang.data+xml'}
HEADERS4 = {'content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'}
payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Basic {auth}',
  'Cookie': cookie
}

class RestconfWebsocketsClient(WebSocketClient):
    def opened(self):
        print("done\n")
        print("Listening for notifications...\n")


    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):

        if str(m)!="X":
            if not os.path.exists('info_logs'):
                os.mkdir('info_logs')
            f=open("/var/www/FailOverQoSDevNet/info_logs/current_alarm.json", "w+")
            f.write(str(m))
            f.close()
            print(m)
            print(info_logs(str(m)))
            p3c=call("python3 alarm_received.py info_logs/current_alarm.json", shell=True)
        else:
            print(str(m))
        #Meter script para que todo lo que cache lo mande a un .txt


if __name__ == '__main__':
    try:
        print("")
        print("\t\t#############################################")
        print("\t\t# CISCO EPN-M RESTCONF NOTIFICATIONS CLIENT #")
        print("\t\t#               WEBSOCKETS                  #")
        print("\t\t#############################################")

        usrPass = username + ":" + password
        byte_usrPass=usrPass.encode("utf-8")
        b64Val = base64.b64encode(byte_usrPass)

        full_url = 'wss://' + ip_epn + '/restconf/streams/v1/alarm.json'

        print("")
        print("Connecting to " + full_url + " ... ", end="")
        ssl_opt={}
        ssl_opt["cert_reqs"] = ssl.CERT_NONE
        ws = RestconfWebsocketsClient(full_url, headers=[('Authorization','Basic %s' % b64Val),('Accept', 'application/json')],ssl_options=ssl_opt)
        ws.connect()
        ws.run_forever()

    
    except KeyboardInterrupt:
        ws.close()
        
    except Exception as err:
        print("\nEntre aqui")
        print(err)
