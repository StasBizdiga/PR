import socket
#import regex as re
import threading
import fncs

def new_client(client,address):
    while True:
        data = client.recv(1024).decode()
        print(">>> Received data %s from %s" % (data,address))
    
        if not(data[1:].replace(" ","").isalnum() and data[0] == "/"): # bool(re.match('^[a-zA-Z0-9]+$',data))
            client.send(
            "Invalid format: Non-alphanumeric.\nClosing connection...\n".encode())
            break # non alphanumeric

        if (data == " "):
            client.send("Write a command! Do you need '/help'?".encode())

        elif (data == "/help"):
            client.send(fncs.help_me())       

        elif (data.split(' ')[0] == "/hello"):
            try:
                temp = data.split(' ')[1:]
                client.send(fncs.hello(temp))  
            except:
                client.send("Please put proper parameters. (ex: /hello text)".encode())

        elif (data.split(' ')[0] == "/prime"):
            try:
                temp = data.split(' ')[1]
                client.send(fncs.is_prime(temp))  
            except:
                client.send("Please put a proper parameter. (ex: /prime 256)".encode())

        elif (data.split(' ')[0] == "/area"):
            try:
                x = data.split(' ')[1]
                y = data.split(' ')[2]
                client.send(fncs.rect_area(x,y))  
            except:
                client.send("Please put proper parameters. (ex: /area 32 79)".encode())


        elif (data == "/answer"):
            client.send(fncs.answer())               
        
        elif (data == "/joke"):
            client.send(fncs.joke())       

        elif (data == "/exit"): 
            client.send("Closing connection...\n".encode())
            break
        
        else:
            client.send("Unknown command. Type '/help'!".encode())

    client.close()

def start_server(address, port, max_connections=5):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(max_connections)
    print("=== Listening for connections at %s:%s" % (address, port))
    while True:
        try:
            client, address = server_socket.accept()
#            client.settimeout(60) # autoclosing connections with inactivity
            print("=== New connection from %s" % (address,))
            threading.Thread(target = new_client,args = (client,address)).start()

        except:
            break
        
    server_socket.close()
            
if __name__ == '__main__':
    start_server('127.0.0.1', 8000)
