import socket
import threading

host = "localhost"
port = 5050
obj = socket.socket()
obj.connect((host, port))

def receive():
    while True:
        message = obj.recv(1024).decode()
        print(f"\n{message}\n", end="Type a Message... ")

def send():
    while True:
        message = input("Type a Message... ")
        if message:
            obj.send(message.encode())
        else:
            obj.close()
            break

thread = threading.Thread(target=receive, args=())
thread.start()
thread2 = threading.Thread(target=send, args=())
thread2.start()