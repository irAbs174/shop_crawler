import socket
import setup
import time

def run_client():
    # client config
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8080
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Establish connection with server
    client.connect((server_ip, server_port))
    try:
        while True:
            # Automatic message to be sent to the server
            msg = "Auto message"
            client.send(msg.encode("utf-8")[:1024])
            # Receive message from the server
            response = client.recv(1024)
            response = response.decode("utf-8")
            # If server sent us "closed" in the payload, break out of the loop and close our socket
            if response.lower() == "closed":
                break
            
            print(f"Received: {response}")
            # Wait for one second before sending the next message
            time.sleep(1)
    finally:
        # Close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()