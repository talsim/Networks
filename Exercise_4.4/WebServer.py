import socket

IP = '0.0.0.0'
PORT = 80


def get_client_request(client):
    """
    Get the client request and spilt it to command(GET) and file path to serve.
    Return the file path
    """
pass


def check_client_request(filePath):
    """
    check if the request(filePath) is Ok and return True.
    otherwise, return False
    """
pass


def generate_headers(response_code):
    """
    Generates the headers for http response
    with the response_code given
    """
pass


def handle_client(filePath_to_serve):
    """
    Main function for handling connected clients and serving files from webroot
    """
pass


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    while True:
        client_socket, address = server_socket.accept()
        request = get_client_request(client_socket)
        if request == '':  # client closed connection
            continue
        valid = check_client_request(request)
        if valid == True:
            handle_client(request)
        else:  # closing the connection
            client_socket.close()


if __name__ == '__main__':
    main()
