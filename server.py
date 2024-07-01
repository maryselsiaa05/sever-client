import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
listener_limit = 5
active_clients = []
clients = []
details = []

def listen_for_message(client,username):
    try:
        while True:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_msg = username+'~'+message
                send_messages_to_all(final_msg)
    except:
        det = details.pop(clients.index(username))
        active_clients.remove((username,client))
        clients.remove(username)
        print(f"Client {det[0]} {det[1]} is Disconnected from the Server")
        prompt_message = "SERVER~"+f"{username} has left from this Chat"
        send_messages_to_all(prompt_message)
        print("Remaining People Strength : "+str(len(clients)))

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message)

def send_message_to_client(client,message):
    message = message+'~'+str(len(active_clients))
    client.sendall(message.encode())

def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            if username in clients:
                c = clients.count(username)
                username = username+f"({c})"
            active_clients.append((username,client))
            clients.append(username)
            prompt_message =  "SERVER~"+f"{username} joined in this Chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_message, args=(client,username, )).start()

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print(f"Running the SERVER on {HOST} {PORT}")
    except:
        print(F"Unable to bind to host {HOST} and port {PORT}")
    server.listen(listener_limit)
    while True:
        client,address = server.accept()
        global host,port
        host = address[0]
        port = address[1]
        details.append((host,port))
        print(details)
        print(f"Successfully connected client {host} {port}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
