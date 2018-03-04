#parsing libraries
from ast import literal_eval  
import xmltodict
import csv

# networking libs
import http.client, urllib

# global result variable
OUTPUT = {"ID":[],"TYPE":[],"VALUE":[]}

def deserialize(data, type):
    if (type == "JSON"):
        return literal_eval(data.decode("utf-8"))

    elif (type == "XML"):
        return xmltodict.parse(data.decode("utf-8"))["device"]

    elif (type == "CSV"):
        d = {'device_id':[],
             'sensor_type':[],
             'value':[]}
        reader = csv.DictReader(data.decode("utf-8").splitlines())        
        for row in reader:
            for key in row:
                d[key].append(row[key])        
        return d
    
    return "not relevant"
    
def save(data,type):
    if (type == "XML"):
        for key in data:
            if key == "@id":
                OUTPUT["ID"].append([data.get(key)])  
            if key == "type":
                OUTPUT["TYPE"].append([data.get(key)])   
            if key == "value":
                OUTPUT["VALUE"].append([data.get(key)])  

    elif (type == "JSON"):
        for key in data:
            if key == "device_id":
                OUTPUT["ID"].append([data.get(key)])  
            if key == "sensor_type":
                OUTPUT["TYPE"].append([data.get(key)]) 
            if key == "value":
                OUTPUT["VALUE"].append([data.get(key)])  
                
    elif (type == "CSV"):
        for key in data:
            if key == "device_id":
                OUTPUT["ID"].append(data.get(key))  
            if key == "sensor_type":
                OUTPUT["TYPE"].append(data.get(key)) 
            if key == "value":
                OUTPUT["VALUE"].append(data.get(key)) 
    
def find_value_format(header):
    for attribute in header:
        for part in attribute:
            if "xml" in part:
                return "XML"
            if "json" in part:
                return "JSON"
            if "csv" in part:
                return "CSV"

no_params = urllib.parse.urlencode({})
mainHeader = {}

Devices = {
    '0' : "Temperature sensors",
    '1' : "Humidity sensors",
    '2' : "Motion sensors",
    '3' : "Alien Presence detectors", 
    '4' : "Dark Matter detectors",
    '5' : "Top Secret detectors"}
    
conn = http.client.HTTPConnection("desolate-ravine-43301.herokuapp.com")

# STEP 1
conn.request("POST", "", no_params, mainHeader)
main_response = conn.getresponse()

#print (response.status, response.reason)
urls = literal_eval(main_response.read().decode("utf-8"))
urls_header = main_response.getheaders() 
secret_key = urls_header[2][1]

print("\nURLs_Header:")
print(urls_header)
print("\nURLs_Body:")
print(urls)
print("\n")

secondaryHeader = { "Session" : secret_key }



"""     MAKE THIS CODE PARALLEL     """
"""|||||||||||||||||||||||||||||||||"""

def test():
    for i in range(len(urls)): 
        try:
            conn.request("GET",urls[i]["path"],no_params, secondaryHeader)
            response = conn.getresponse()
            
            h = response.getheaders()
            raw_data = response.read() 
            value_format = find_value_format(h)
            device_body = deserialize(raw_data,value_format)
            save(device_body, value_format)
            
            #print("Device header\n",h)
            print(i+1,") Device Body\n",device_body)
            print("ValueFormat: ",value_format,"\n")
           # while(True):    #forcing a http exception
            #    response = conn.getresponse()
    
        except  http.client.HTTPException as e:
            print("!!! SERVER KEY TIMED OUT!!!")
            # NEED TO RETURN TO STEP 1
            return("HTTPException")

"""|||||||||||||||||||||||||||||||||"""
test()
#######################################

print("output: ",OUTPUT["TYPE"])
L1 = [item for sublist in OUTPUT["ID"] for item in sublist]
L2 = [item for sublist in OUTPUT["TYPE"] for item in sublist]
L3 = [item for sublist in OUTPUT["VALUE"] for item in sublist]
FINAL = {"ID":L1,"TYPE":L2,"VALUE":L3}
print("Final:",FINAL)
print("\n- RESULTS -")
for i in range(len(Devices)):
    t=0;
    print("\n",Devices[str(i)],": ") # group name
    for j in FINAL["TYPE"]:
        if j == str(i) or j==i:
            print("Device-|",FINAL["ID"][t],"|:",FINAL["VALUE"][t])
        t+=1 
conn.close()


import pip 
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in installed_packages]) 
print(installed_packages_list)


