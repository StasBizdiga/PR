import socket


def start_client(address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    print("=== Connected to %s:%s" % (address, port))
    while True:
        try:
            data = input(">>> ")
            if data == '':
                data = " "
            client_socket.send(data.encode())
            data = client_socket.recv(1024)
            print("<<< %s" % (data.decode(),))
            if ("Closing connection...".encode() in data):
                break
        except:
            break
        
    client_socket.close()


if __name__ == '__main__':
    start_client('127.0.0.1', 8000)