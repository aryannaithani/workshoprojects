import socket
import threading

clients = []
host = "localhost"
port = 5050
server = socket.socket()
server.bind((host, port))
server.listen()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, serial):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[Client-{serial}] : {message}")
            broadcast_msg = f"[Client-{serial}] : {message}"
            broadcast(broadcast_msg, client_socket)
        except:
            print(f"Client-{serial} disconnected.")
            clients.remove(client_socket)
            break
    client_socket.close()

print("Server is listening...")
while True:
    conn, address = server.accept()
    print(f"Connected with {str(address)}")
    clients.append(conn)
    sr_num = str((clients.index(conn)) + 1)
    thread = threading.Thread(target=handle_client, args=(conn,sr_num,))
    thread.start()