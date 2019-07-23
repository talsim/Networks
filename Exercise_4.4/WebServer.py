import socket

IP = '0.0.0.0'
PORT = 80

def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    done = False
    while not done:
        if

if __name__ == '__main__':
    main()
