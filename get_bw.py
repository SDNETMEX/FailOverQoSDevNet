import requests
import os


ip_epn = os.environ['IP_EPN']
auth = os.environ['AUTH_EPN']
cookie = os.environ['COOKIE']

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Basic {auth}',
  'Cookie': cookie
}

def getBESpeed(hostname,bundleid):
  
  url = "https://"+ip_epn+"/restconf/data/v1/cisco-resource-ems:termination-point?" \
  "fdn=MD=CISCO_EPNM!ND=" + hostname + "!FTP=name=Bundle-Ether"+bundleid+";lr=lr-lag-fragment"
  response = requests.request("GET", url, headers=headers, data = payload,  verify=False)
  json_req_be_speed = response.json()["com.response-message"]["com.data"]["tp.termination-point"]["tp.if-speed"]
  return json_req_be_speed

def getBETraffic(hostname,bundleid,start_t,end_t):

  url = "https://"+ip_epn+"/webacs/api/v2/op/statisticsService/interfaces/metrics/" \
  "outtraffic?startTime=" + start_t + "&endTime=" + end_t + "&metricDataType=TIME_SERIES&device=" + hostname + "&ifName=Bundle-Ether"+bundleid

  response = requests.request("GET", url, headers=headers, data = payload,  verify=False)
  print(response.text)
  try:
    json_req_t = response.json()["mgmtResponse"]["metricData"][0]["yvalueProperty"]["yvalueProperty"][0]["maxVal"]
    return json_req_t
  except:
    return 400

def getBEMembers(hostname,bundleid):
  url = "https://"+ip_epn+"/restconf/data/v1/cisco-resource-ems:termination-point?" \
  "fdn=MD=CISCO_EPNM!ND=" + hostname + "!FTP=name=Bundle-Ether"+bundleid+";lr=lr-lag-fragment"

  response = requests.request("GET", url, headers=headers, data = payload,  verify=False)
    
  return response.text.encode('utf8')