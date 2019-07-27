import socket
import os
from pathlib import Path
from datetime import datetime

IP = '0.0.0.0'
PORT = 80


def get_client_request(client):
    """
    Get the client request and spilt it to command(GET) and file path to serve.
    Return the file path
    """
    req = client.recv(1024).decode()
    print(f'request = {req}')
    if req == '':
        return [None, '']
    string_list = req.split(' ')  # Split request from spaces
    method = string_list[0]  # First string is the method
    fileName = string_list[1]  # Second string is the requested file
    fileName = fileName.split('?')[0]  # if GET has parameters ('?), ignore them
    current_dir = Path.cwd()
    if fileName == '/':
        filePath = current_dir / 'webroot' / 'index.html'  # Load index file as root
    else:
        print(f'\ncurrent_dir = {current_dir}\n')
        print(f'\nfileNmae = {fileName}\n')
        filePath = current_dir / 'webroot' / fileName
    return [filePath, method]


def check_given_method(method):
    """
    Check if the given method is GET (only GET supported)
    """
    if method == "GET":
        return True
    return False

def generate_headers(code, filePath = None):
    """
    Generates the headers for http response
    with the code given
    """
    header = ''
    mimetype = ''
    if code == '200':
        header += 'HTTP/1.1 200 OK\n'
        header += f'Content-Length: {os.path.getsize(filePath)}\n'
        if str(filePath).endswith(('.txt', '.html')):
            mimetype = 'text/html; charset=utf-8'
        elif str(filePath).endswith('.jpg'):
            mimetype = 'image/jpg'
        elif str(filePath).endswith('.js'):
            mimetype = 'text/javascript; charset=UTF-8'
        else:  # (.css)
            mimetype = 'text/css'
    elif code == '404':
        header += 'HTTP/1.1 404 Not Found\n'
    header += f'Date: {datetime.now()}\n'
    header += 'Server: Gvahim Http WebServer\n'
    header += f'Content-Type: {mimetype}\n\n'
    print(f'\nheader = {header}')
    return header



def handle_client(code, client, filePath_to_serve = None):
    """
    Main function for handling connected clients and serving files from webroot
    """
    if code == '200':
        file = open(filePath_to_serve, 'rb')
        response_data = file.read()
        file.close()
        header = generate_headers(code, filePath_to_serve)
    elif code == '404':
        response_data = '404 Error: Page not found'
        header = generate_headers(code)
    response = str(header).encode()
    response += str(response_data).encode()
    print(f'response = {response.decode()}')
    client.sendall(response)

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
        if method == '':
            client_socket.close()
            continue
        print(f'filePath: {filePath}\nmethod: {method}')
        valid_method = check_given_method(method)
        if valid_method:
            file_exist = os.path.isfile(filePath)
            if file_exist:
                handle_client('200', client_socket, filePath)
            else:  # file doesn't exist
                handle_client('404', client_socket)
        else:  # method not valid (only GET method supported)
            client_socket.close()


if __name__ == '__main__':
    main()