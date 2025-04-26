import socket

# Server Details
Address = '127.0.0.1'
Port = 8888

# Create socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Address, Port))

print("Socket connected")
client_socket.close()
 
