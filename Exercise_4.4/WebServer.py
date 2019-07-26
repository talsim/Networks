import socket
import os

IP = '0.0.0.0'
PORT = 80


def get_client_request(client):
    """
    Get the client request and spilt it to command(GET) and file path to serve.
    Return the file path
    """
    req = client.recv(1024).decode()
    string_list = req.split(' ')  # Split request from spaces
    method = string_list[0]  # First string is the method
    fileName = string_list[1]  # Second string is the requested file
    fileName = fileName.split('?')[0]  # if GET has parameters ('?), ignore them
    current_dir = os.getcwd()
    if fileName == '/':
        filePath = f'{current_dir}\\webroot\\index.html'  # Load index file as root
    else:
        filePath = f'{current_dir}\\webroot\\{fileName}'
    return [filePath, method]


def check_given_method(method):
    """
    Check if the given method is GET (only GET supported)
    """


def generate_headers(code):
    """
    Generates the headers for http response
    with the code given
    """
    pass


def handle_client(code, filePath_to_serve=''):
    """
    Main function for handling connected clients and serving files from webroot
    """
    pass


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    print('Listening')
    while True:
        client_socket, address = server_socket.accept()
        print(f'Client connected from: {address}')
        filePath, method = get_client_request(client_socket)
        print(f'filePath: {filePath}\nmethod: {method}')
        valid_method = check_given_method(method)
        if valid_method:
            file_exist = os.path.isfile(filePath)
            if file_exist:
                handle_client('200', filePath)
            else:  # file doesn't exist
                handle_client('404')
        else:  # method not valid (only GET method supported)
            client_socket.close()


if __name__ == '__main__':
    main()
