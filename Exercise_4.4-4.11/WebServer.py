import socket
import os
import logging
import WebFunctions
from http import HTTPStatus
from pathlib import Path
from datetime import datetime

IP = '0.0.0.0'
PORT = 80


def get_client_request(client):
    """
    Get the client request and spilt it to command(GET) and file path to serve.
    Return the file path and the method
    """
    req = client.recv(1024)
    if req == b'':
        return None

    req_content = req.split(b'\r\n\r\n')[0].decode()
    string_list = req_content.split(' ')  # Split request from spaces
    method = string_list[0]  # First string is the method
    addr = string_list[1]  # Second string is the address
    if '?' not in addr:  # GET doesn't have any parameters (means addr is a file)
        current_dir = Path.cwd()
        file_name = addr
        if file_name == '/':
            file_path = current_dir / 'webroot' / 'index.html'  # Load index file as root
        else:
            file_name = file_name.replace("/", os.sep)  # replacing all the separators with the ones similar to the OS
            file_path = f'{current_dir}{os.sep}webroot{file_name}'
        return [file_path, method]
    func = addr.split('?')[0].split('/')[1].replace('-', '_')
    logging.info(f'func = {func}')
    params = addr.split('?', 1)[1]  # GET parameters
    if '&' not in params:  # only one parameter
        params = params.split('=')[1]
    logging.info(f'params = {params}')
    return [addr, method, func, params, req]


def check_given_method(method):
    """
    Check if the given method is valid (GET or POST)
    """
    if method == "GET" or method == "POST":
        return True
    return False


def get_mimetype(file_path):
    """
    Get mimetype for generating the headers.

    Parameters:
        file_path - the file path.
    Returns:
        mimetype - the correct mimetype to generate the headers with.
    """
    file_path = str(file_path)
    if file_path.endswith(('.txt', '.html')):
        mimetype = 'text/html; charset=utf-8'
    elif file_path.endswith('.jpg'):
        mimetype = 'image/jpg'
    elif file_path.endswith('.js'):
        mimetype = 'text/javascript; charset=UTF-8'
    elif file_path.endswith('.css'):
        mimetype = 'text/css'
    elif file_path.endswith('.ico'):
        mimetype = 'image/x-icon'
    elif file_path.endswith('.gif'):
        mimetype = 'image/gif'
    else:
        mimetype = 'text/plain'
    return mimetype


def generate_headers(status_code, file_path=None, data=None):
    """
    Generates the headers for http response
    with the status_code given
    """
    header = ''
    if status_code == HTTPStatus.OK.value:
        header += 'HTTP/1.1 200 OK\n'
        if data is not None:
            header += f'Content-Length: {len(str(data))}\r\n'
            header += 'Content-Type: text/plain\r\n'
        elif file_path is not None:
            header += f'Content-Length: {os.path.getsize(file_path)}\r\n'
            header += f'Content-Type: {get_mimetype(file_path)}\r\n'
    elif status_code == HTTPStatus.NOT_FOUND.value:
        header += 'HTTP/1.1 404 Not Found\r\n'
    header += f'Date: {datetime.now()}\r\n'
    header += 'Server: Gvahim Http WebServer\r\n\r\n'
    logging.info(f'\nheader = {header}')
    return header


def handle_client(status_code, client, func=None, file_path_to_serve=None, params=None, req=None):
    """
    Main function for handling connected clients and serving files from webroot
    """
    if status_code == HTTPStatus.OK.value:  # 200
        if file_path_to_serve is not None:
            with open(file_path_to_serve, 'rb') as file:
                response_data = file.read()
            header = generate_headers(status_code, file_path_to_serve)
        elif params is not None:
            if func == 'upload':
                # params = f'<file_name>{params}</file_name> <client>{client}</client> <request>{req}</request>' # adding additional parameters that upload function requires
                response_data = getattr(WebFunctions, func)(params, client, req)
            else:
                response_data = getattr(WebFunctions, func)(params)
            header = generate_headers(status_code, data=response_data)
            response_data = str(response_data).encode()
            logging.info(f'DATA: {response_data}')
    elif status_code == HTTPStatus.NOT_FOUND.value:  # 404
        response_data = '404 Error: NOT FOUND'
        header = generate_headers(status_code)
    response = str(header).encode()
    response += response_data
    client.sendall(response)


def _listen():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    return server_socket


# req_list[0] = address
# req_list[1] = method
# req_list[2] = function
# req_list[3] = params
def main():
    server_socket = _listen()
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')  # init
    while True:
        logging.info('Waiting for client')
        client_socket, address = server_socket.accept()
        logging.info(f'Client connected from: {address}')
        req_list = get_client_request(client_socket)
        if req_list == None:
            logging.info('Client disconnected')
            continue
        logging.info(f'address: {req_list[0]}\nmethod: {req_list[1]}')
        valid_method = check_given_method(req_list[1])
        if valid_method:
            if len(req_list) > 2:  # if there is parameters, pass it to handle_client()
                handle_client(200, client_socket, func=req_list[2], params=req_list[3], req=req_list[4])
            elif os.path.isfile(req_list[0]):  # if file exist
                handle_client(200, client_socket, file_path_to_serve=req_list[0])
            else:  # file doesn't exist
                handle_client(404, client_socket)
        else:  # method not valid (only GET method supported)
            client_socket.close()


if __name__ == '__main__':
    main()
