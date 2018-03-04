# user files
import utils 

# networking libs
import http.client
import urllib,urllib.request as r

# utils
from ast import literal_eval 

# parallel programming lib 
import threading
        
def step1():
    conn.request("POST", "")
    main_response = conn.getresponse()
    
    #print (response.status, response.reason)
    urls = literal_eval(main_response.read().decode("utf-8")) #response to dict
    urls_header = main_response.getheaders() 
    urls_range = list(range(len(urls)))
    secret_key = urls_header[2][1]
    
    debug_data(urls,urls_header)
    
    secondaryHeader = { "Session" : secret_key }
    return urls,secondaryHeader,len(urls_range)

def debug_data(urls,urls_header):
    print("\nURLs_Header:")
    print(urls_header)
    print("\nURLs_Body:")
    print(urls)
    print("\n")

def step2(urls_count):
    urls_clean = []
    for i in range(urls_count):
        urls_clean.append("http://"+URL+urls[i]["path"])
    return urls_clean
    
def fetch_url(url):
    try:
        req = r.Request(url,b'',secondaryHeader)
        result = r.urlopen(req).read().decode("utf-8")
        process_result(result)

#       result_h = r.urlopen(req).info().items() # header
#       print("result:\n",result)   # for debugging

    
    except  urllib.error.HTTPError as e:
        print("!!! SERVER KEY TIMED OUT!!!")
        #step1() #repeat step1
        print(e)
        return 0,0
   

def multiple_requests(urls):
    threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def process_result(result):

    value_format = utils.guess_value_format(result)
    device_body = utils.deserialize(result,value_format)
    utils.save(device_body, value_format)
    
    print("HTTP Request successful!")
    print("Device Body\n",device_body)
    print("ValueFormat: ",value_format,"\n")   
    
    
URL = "desolate-ravine-43301.herokuapp.com"
conn = http.client.HTTPConnection(URL)

"""# STEP 1"""
urls,secondaryHeader,urls_count = step1()
"""# STEP 2"""
urls = step2(urls_count)
"""# STEP 3"""
multiple_requests(urls)

utils.format_and_reorder_output()    
conn.close()


