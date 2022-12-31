import socket
import threading
import time
import webbrowser

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def keepalive():
    print(threading.current_thread())
    while True:
        # Send the "keep alive" message every 5 seconds
        sock.sendall(b'keep alive')
        print("sent keep alive to server")
        time.sleep(2)


# Connect the socket to the port where the server is listening
server_address = ('localhost', 3000)
print(f'connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)
keepThread = threading.Thread(target=keepalive)
keepThread.start()


def weblink(msg):
    webbrowser.open("http://", msg[2::1])

while True:
    msg = sock.recv(1024).decode()
    print(msg)
    if msg != 'quit' and msg != '':
            if msg[0] == '3':
                weblink(msg)
    else:
        break

sock.close()