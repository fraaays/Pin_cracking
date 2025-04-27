import socket

# Server Details
Address = '127.0.0.1'
Port = 8888

for pin in range(0, 1000):
    formatted_pin = f"{pin:03d}"
    print(f"Testing PIN: {formatted_pin}")

# Create socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Address, Port))

body = f"magicNumber={formatted_pin}"
request = (
    f"POST /verify HTTP/1.1\r\n"
    f"Host: {Address}:{Port}\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(body)}\r\n"
    "Connection: close\r\n"
    "\r\n"
    f"{body}"
)

client_socket.sendall(request.encode())


print("Socket connected")
client_socket.close()
 
