'''
Name : Mohamad Ali Salhab
ID : 201900111
Username : mas164

I, Mohamad Ali Salhab , am the author of this program.


This program represents the client, and is mainly working to send data to server.py which analyze the value and works accordingly except for put 
and get where they require some work in this code. 

This program requires: IP, PORT and Debug value before running.

'''
import socket, os, sys

IP = sys.argv[1]
PORT = int(sys.argv[2])
DEBUG = int(sys.argv[3])

ADDR = (IP, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while True:
    data = client.recv(BUFFER_SIZE).decode(FORMAT)
    command, message = data.split("+")

    if command == "DISCONNECTED":
        if DEBUG==1:
            print(f"[SERVER]: {message}")
        elif DEBUG==0:
            pass
        else:
            print("Debug mode can either be 0 or 1 not: ",DEBUG)
        
        break
    
    elif command == "OK":
        if DEBUG==1:
            print(f"{message}")
        elif DEBUG==0:
            pass
        else:
            print("Debug mode can either be 0 or 1 not: ",DEBUG)

    data = input("> ")
    data = data.split(" ")
    command = data[0]

    if command == "help":
        opcode = '011'
        messagetosend = opcode
        client.send(messagetosend.encode(FORMAT))
    
    elif command == "bye":
        opcode = '0'
        messagetosend = opcode
        client.send(messagetosend.encode(FORMAT))
        break
    
    elif command == "get":
    
        op = '001'
        opcode = str.encode(op)

        filename = data[1]

        FL = "{0:b}".format(len(filename)).zfill(5)
        FL = str.encode(FL)
        FN = str.encode(filename)

        messagetosend = bytearray(opcode + FL + FN )

        client.send(messagetosend)

        
        with open(filename, "wb") as f:
            # print("File opened to write")
            while True:
                # print("Writing data")
                bytesread = client.recv(BUFFER_SIZE)
                if not bytesread:
                    break
                f.write(bytesread)
                break
            # print("data written")


    elif command == "change":

        op = '010'
        
        opcode = str.encode(op)

        filename = data[1]
        newfilename = data[2]

        OFL = "{0:b}".format(len(filename)).zfill(5)
        OFL = str.encode(OFL)
        OFN = str.encode(filename)

        NFL = "{0:b}".format(len(newfilename)).zfill(8)
        NFL = str.encode(NFL)
        NFN = str.encode(newfilename)

        messagetosend = bytearray(opcode + OFL + OFN + NFL + NFN)

        client.send(messagetosend)


    elif command == "put":

        op = '000'
        opcode = str.encode(op)

        filename = data[1]
        FS = str(os.path.getsize(filename))
        FS = str.encode(FS)

        FL = "{0:b}".format(len(filename)).zfill(5)
        FL = str.encode(FL)
        FN = str.encode(filename)

        messagetosend = bytearray(opcode + FL + FN + FS)

        client.send(messagetosend)
        
        
        with open(filename,"rb") as f:
            # print("Opened file")
            while True:
                # print("Sending")
                bytesread = f.read(BUFFER_SIZE)
                if not bytesread:
                    break
                client.sendall(bytesread)
            # print("Sent")
        # print("Done")

print("Disconnected from the server.")
client.close()
