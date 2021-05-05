# Local-File-Transfer-Service
Networking app using python socket programming, 


1-	Go to server_data, run: python server.py 1 
python server.py 1 means debug mode on
python server.py 0 means debug mode off

2-	Go to client_data, run: python client.py 192.168.0.100 5050 1
python client.py 192.168.0.100 5050 1 means debug mode on
python client.py 192.168.0.100 5050 0 means debug mode off
Note that 192.168.0.100 means the local ipv4 and 5050 is the port which are already set in server_data/server.py
Note that 192.169.0.100 may change according to your ipv4 connection.

3-	Run commands (help, put, get, bye, change) and the file will execute them normally

![image](https://user-images.githubusercontent.com/83377546/117171618-b1f10700-add3-11eb-8f72-6964e4ae07a5.png)
