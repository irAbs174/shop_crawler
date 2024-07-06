import socket
import threading
import time

def handle_client(client_socket):
    client_socket.send("174".encode('utf-8'))
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"CLIENT_MSG => {message.encode('utf-8')}")
            if message == "TARGET_ADDRESS":
                response = "TARGET_ADDRESS_DATA"
                client_socket.send(response.encode('utf-8'))
            elif message == "=> ******** END ******** <=":
                
                response = "0"
                client_socket.send(response.encode('utf-8'))
            else:
                print(f"Client Received => {message.encode('utf-8')}")
                response = "=>>>> END <<<<="
                client_socket.send(response.encode('utf-8'))
        except:
            break
    client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind(('0.0.0.0', 8778))
    client.listen(5)
    print("SERVER started, waiting for connections...")
    
    while True:
        client_socket, addr = client.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_client()