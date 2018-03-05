# user files
import utils 

# networking libs
import http.client
import urllib,urllib.request as r


# utils
import time
from ast import literal_eval 

# parallel programming libs
import threading as t
        
def parallel_t_requests(urls):
    threads = [t.Thread(target=fetch_url, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()        
        
def main_request(debug_mode):
    conn.request("POST", "")
    main_response = conn.getresponse()
    
    """http.response (byte) to string, then to dict:"""
    urls_body = literal_eval(main_response.read().decode("utf-8")) 
    urls_header = main_response.getheaders() 
    urls_count = len(urls_body)
    secret_key = urls_header[2][1]
   
    if(debug_mode):
        utils.debug_data(urls_body,urls_header)
    
    secret_key_header = { "Session" : secret_key }
    return urls_body,secret_key_header,urls_count


def refactor_urls(urls_count,urls_body,URL):
    urls_clean = []
    for i in range(urls_count):
        urls_clean.append("http://"+URL+urls_body[i]["path"])
    return urls_clean
    
def fetch_url(url):
    #print("HTTP request sent!")
    try:
        s1 = time.time() 
#----------------------------
        req = r.Request(url,b'',secret_key_header)
        result = r.urlopen(req).read().decode("utf-8")
#        result_h = r.urlopen(req).info().items() # header, if required
        process_result(result)
#----------------------------        
        e1 = time.time()
        
        print("Response time:",e1 - s1)

    
    except urllib.error.HTTPError as e:
        print("\n!!! SERVER KEY TIMED OUT!!!")
        print("Or perhaps:",e)
        e1 = time.time() #time when the failed request would've finished
        print("FAILED Response time:",e1 - s1)        
        retrying = True
    

def process_result(result):

    value_format = utils.guess_value_format(result)
    device_body = utils.deserialize(result,value_format)
    utils.save(device_body, value_format)
    
    print("\nHTTP Response successful!") #debug
    print("Device Body\n",device_body)   #debug
    print("ValueFormat: ",value_format)  #debug


URL = "desolate-ravine-43301.herokuapp.com"
conn = http.client.HTTPConnection(URL)
retrying = True #only first time
while(retrying):
    
    """# STEP 1"""
    urls_body,secret_key_header,urls_count = main_request(True)
    """# STEP 2"""
    urls = refactor_urls(urls_count,urls_body,URL)
    """# STEP 3"""
    retrying = False #job considered complete...
    parallel_t_requests(urls)    
    if(retrying): #...unless an error requests a retry
        print("\n!!! RETRYING !!!")
    
    
"""# STEP omega"""
utils.format_and_reorder_output()    
conn.close()


