'''
Name : Mohamad Ali Salhab
ID : 201900111
Username : mas164

I, Mohamad Ali Salhab , am the author of this program.


This program initiates the server, and classifies each conmand sent by the server and works accordingly.
This program requires a debug_mode value before running.

'''
import os, socket, threading, sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
DEBUG = int(sys.argv[1])
ADDR = (IP, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 4096

def handle_client(conn, addr):
    if DEBUG==1:
        print(f"[NEW CONNECTION] {addr} connected.")
    elif DEBUG==0:
        pass
    else:
        print("Debug mode can either be 0 or 1 not: ",DEBUG)
    
    conn.send("OK+Session has been established.".encode(FORMAT))

    while True:
        data = conn.recv(BUFFER_SIZE)
        # data = data.split("+")
        # conmand = data[0]

        data = data.decode()

        opcode = data[0:3]

        if opcode == "001":
            #get

            FL = data[3:8]
            FN = data[8:8+(int(FL,2))]

            # print("File details received")
            with open(FN, "rb") as f:
                # print("File opened to read")
                while True:
                    # print("Sending data")
                    bytesread = f.read(BUFFER_SIZE)
                    if not bytesread:
                        break
                    conn.sendall(bytesread)
                    break
                break
                # print("Data sent")
            
            send_data = "OK+File downloaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif opcode == "000":
            #put

            FL = data[3:8]
            FN = data[8:8+(int(FL,2))]

            with open(FN, "wb") as f:
                # print("opened file")
                while True:
                    # print("Sending")
                    bytesread = conn.recv(BUFFER_SIZE)
                    f.write(bytesread)
                    if not bytesread:
                        break
                    break
            
            send_data = "OK+File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif opcode == "010":
            #change
            # filename, newfilename = data[1], data[2]
            files = os.listdir()
            send_data = "OK+"

            OFL = data[3:8]
            OFN = data[8:8+(int(OFL,2))]
            
            NFL = data[7+(int(OFL,2)) : 16+(int(OFL,2))]
            NFN = data[16+(int(OFL,2)) :]

            # NFL = data[OFL:OFL+9]
            # NFL = int(NFL,2)
            # NFN = data[OFL+8:].decode()

            if len(files) == 0:
                send_data += "There is no files in the server"
            else:
                os.rename(OFN,NFN)
                #change name from Old file name to New file name
                send_data += "Filename changed successfully"
            
            conn.send(send_data.encode(FORMAT))


        elif opcode == "0":
            #bye
            break
        
        elif opcode == "011":
            #help
            data = "OK+"
            data += "Conmands are: bye change get help put"

            conn.send(data.encode(FORMAT))
        
    if DEBUG==1:
        print(f"[DISCONNECTED] {addr} disconnected")
    elif DEBUG==0:
        pass
    else:
        print("Debug mode can either be 0 or 1 not: ",DEBUG)
        
        conn.close()

if DEBUG==1:
    print("[STARTING] Server is starting")
elif DEBUG==0:
    pass
else:
    print("Debug mode can either be 0 or 1 not: ",DEBUG)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

if DEBUG==1:
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
elif DEBUG==0:
    pass
else:
    print("Debug mode can either be 0 or 1 not: ",DEBUG)


while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    
    if DEBUG==1:
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    elif DEBUG==0:
        pass
    else:
        print("Debug mode can either be 0 or 1 not: ",DEBUG)
    
