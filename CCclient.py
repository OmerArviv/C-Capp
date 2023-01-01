import socket
import threading
import time
import webbrowser
from datetime import datetime
import json


def keepalive():         # keep alive thread
    print(threading.current_thread())
    while True:
        # Send the "keep alive" message every katime seconds
        sock.sendall(b'keep alive')
        print("sent keep alive to server")
        time.sleep(katime)




def weblink(msg):             #function who opens link in the browser for the client
    #webbrowser.open("http://", msg[2::1])
    url=msg[2::1]
    print(url)
    new = 2  # open in a new tab, if possible
    webbrowser.open(url, new=new)


def portscanclient(msg):       #function that runs a port scan to the client and send the info to the server
    remote_server = msg[2::1]
    remoteServerIP = socket.gethostbyname(remote_server)
    msg = "Please wait remote host " + remoteServerIP
    time.sleep(2)
    sock.send(msg.encode())
    msg = sock.recv(1024).decode()
    endMessage = "Port Scanning results:\n"
    if msg == 'ok':
        t1 = datetime.now()
        try:
            for port in range(startport, endport):
                print(port)
                tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tempSocket.settimeout(0.0001)
                result = tempSocket.connect_ex((remoteServerIP, port))
                if result == 0:
                    endMessage += "Port " + str(port) + ":    Open\n"
                tempSocket.close()
        except KeyboardInterrupt:
            msg = "Client pressed Ctrl+C"
            sock.send(msg.encode())
        except socket.gaierror:
            msg = "Couldn't connect to server"
        t2 = datetime.now()
        totalTime = t2 - t1
        if endMessage == "Port Scanning results:\n":
            endMessage += "No ports are open between 0-5000\n"
        endMessage += "Scanning completed in "+ str(totalTime)
        sock.send(endMessage.encode())


with open("configuration.json") as json_file:
    data = json.load(json_file)

if data['port'] :                     #get the information from configuration.json
    port_number=data['port']
else:
    port_number = 3000

if data['katime']:
    katime=data['katime']
else:
    katime=2

if data['startport']:
    startport=data['startport']
else:
    startport=0

if data['endport']:
    endport=data['endport']
else:
    endport=500


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', port_number)
print(f'connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)
keepThread = threading.Thread(target=keepalive)
keepThread.start()

while True:               #getting the messages for the server
    msg = sock.recv(1024).decode()
    if msg != 'quit' and msg != '':
        if msg[0] == '3':
            weblink(msg)
        elif msg[0] == '4':
            portscanclient(msg)
    else:
        break

sock.close()