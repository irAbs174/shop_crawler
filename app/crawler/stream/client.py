import socket
import threading
import time

def send_message(server_socket):
    while True:
        response = server_socket.recv(1024).decode('utf-8')
        print(f"SERVER_MSG => {response}")
        if response == "174":
            message = "TARGET_ADDRESS"
            server_socket.send(message.encode('utf-8'))
        elif response == "TARGET_ADDRESS_DATA":
            message = "=> ******** END ******** <="
            server_socket.send(message.encode('utf-8'))
        else:
            message = "=>>>> END <<<<="
            server_socket.send(message.encode('utf-8'))
        time.sleep(5)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('127.0.0.1', 8778))
    print("Connected to the server.")
    
    message_sender = threading.Thread(target=send_message, args=(server,))
    message_sender.start()

if __name__ == "__main__":
    start_server()
