#parsing libraries
from ast import literal_eval  
import xmltodict
import csv

# global result variable
OUTPUT = {"ID":[],"TYPE":[],"VALUE":[]}

Devices = {
    '0' : "Temperature sensors",
    '1' : "Humidity sensors",
    '2' : "Motion sensors",
    '3' : "Alien Presence detectors", 
    '4' : "Dark Matter detectors",
    '5' : "Top Secret detectors"}
    
def deserialize(data, type):
    if (type == "JSON"):
        return literal_eval(data)

    elif (type == "XML"):
        return xmltodict.parse(data)["device"]

    elif (type == "CSV"):
        d = {'device_id':[],
             'sensor_type':[],
             'value':[]}
        reader = csv.DictReader(data.splitlines())        
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
    return None
    
def guess_value_format(data):
    for attribute in data:
        for part in attribute:
            if "<" in part:
                return "XML"
            if "{" in part:
                return "JSON"
            if "," in part:
                return "CSV"
    return None
                
def debug_data(urls_body,urls_header):
    print("\nURLs_Header:")
    print(urls_header)
    print("\nURLs_Body:")
    print(urls_body)
    print("\n")
    
def format_and_reorder_output():
    #Collecting raw data (list with lists)
    L1 = [item for sublist in OUTPUT["ID"] for item in sublist]
    L2 = [item for sublist in OUTPUT["TYPE"] for item in sublist]
    L3 = [item for sublist in OUTPUT["VALUE"] for item in sublist]
    
    #Storing collected data into a dict
    FINAL = {"ID":L1,"TYPE":L2,"VALUE":L3}
    
    print("\n- RESULTS -")
    for i in range(len(Devices)):
        t=0;
        print("\n",Devices[str(i)],": ") #device name
        for j in FINAL["TYPE"]:
            if j == str(i) or j==i: #ordering data by device type
                print("Device-|",FINAL["ID"][t],"|:",FINAL["VALUE"][t])
            t+=1 