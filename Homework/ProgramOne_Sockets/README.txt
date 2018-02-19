Initialize the server program first:

Port number can be changed in the Server.py file.

usage: python3 Server_Main.py 


Initialize the client program:

Server-delay can be manually configured in Client.py file.

I chose to not take user input for things like message size and server delay for each
round of data transfer because it was tedious. Instead, it is automated and will run through
15 transfers of each specified data size. The functionality to take user input is included in the 
program, but you will have to uncomment it. It is in the build_startup_message function.

usage: python3 Client_Main.py <IP> <PORT>