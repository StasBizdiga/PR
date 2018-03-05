# user files
import utils 

# networking libs
import http.client
import urllib,urllib.request as r

# utils
import time
from ast import literal_eval 

# parallel programming lib 
import threading
        
def step1(is_viewable):
    conn.request("POST", "")
    main_response = conn.getresponse()
    
    #print (response.status, response.reason)
    urls = literal_eval(main_response.read().decode("utf-8")) #response to dict
    urls_header = main_response.getheaders() 
    urls_range = list(range(len(urls)))
    secret_key = urls_header[2][1]
   
    if(is_viewable):
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
    
    #print("HTTP Response sent!")
    try:        
        s1 = time.time()

        req = r.Request(url,b'',secondaryHeader)
        result = r.urlopen(req).read().decode("utf-8")
        process_result(result)
        
        e1 = time.time()
        
        
        print("Response time:",e1 - s1)
#       result_h = r.urlopen(req).info().items() # header
#       print("result:\n",result)   # for debugging
        start_over = False
    
    except  urllib.error.HTTPError as e:
        print("\n!!! SERVER KEY TIMED OUT!!!")
        print(e)
        
        e1 = time.time()
        print("FAILED Response time:",e1 - s1)
        
        start_over = True
        
        return 0,0

def parallel_requests(urls):
    threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


#def linear_requests(urls):
#    [fetch_url(url) for url in urls]

def process_result(result):

    value_format = utils.guess_value_format(result)
    device_body = utils.deserialize(result,value_format)
    utils.save(device_body, value_format)
    
    print("\nHTTP Response successful!")
    print("Device Body\n",device_body)
    print("ValueFormat: ",value_format)   


URL = "desolate-ravine-43301.herokuapp.com"
conn = http.client.HTTPConnection(URL)
start_over = True

while(start_over):
    """# STEP 1"""
    urls,secondaryHeader,urls_count = step1(True)
    """# STEP 2"""
    urls = step2(urls_count)
    """# STEP 3"""
    parallel_requests(urls)
    #linear_requests(urls)
    io = input("\nRetry? (y/n):")
    if (io=="y"):
        start_over = True
        print("\n!--- R E T R Y I N G ---!\n")
    else:
        start_over = False    

"""# STEP omega"""
utils.format_and_reorder_output()    
conn.close()


