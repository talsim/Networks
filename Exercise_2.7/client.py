import socket
from random import randint

IP = '127.0.0.1'
PORT = 8820
requests = ['TAKE_SCREENSHOT', 'DIR', 'SEND_FILE', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']


def valid_request(request):
    """Check if the request is valid (is included in the available commands)
    Return:
        True if valid, False if not
    """
    request = request.rsplit(' ')[0]  # the command
    request = request.upper()
    return request in requests


def send_request_to_server(my_socket, request):
    """Send the request to the server. First the length of the request (2 digits), then the request itself

    Example: '04EXIT'
    Example: '12DIR c:\cyber'
    """
    length = str(len(request)).zfill(2)  # add zero to the start of the number if it is one digit
    full_request = length + request  # building the request
    my_socket.send(full_request.encode())


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    message = my_socket.recv(1024)
    if message == 'file transfer'.encode():
        ext_n_size = my_socket.recv(1024).decode()
        f_size = int(ext_n_size.split()[1])
        extension = ext_n_size.split()[0]
        if ext_n_size.startswith('png'):  # picture
            f = open(f'new_screenshot{randint(1, 100)}.{extension}', 'wb')
        else:  # file
            f = open(f'new_{request.rsplit()[1].lower()}', 'wb')
        my_socket.send(b'GOT EXT AND SIZE')
        RECV_FILE(f, f_size, my_socket)
        f.close()

    else:
        print(f'Server response: {message.decode()}')


def RECV_FILE(f, size, s):
    """ RECV_FILE gets the file and the file size

    he receives the file data in small parts and when finished,
    he prints "Download Complete!"
    """
    data = s.recv(1024)
    total_recv = len(data)
    f.write(data)
    while total_recv < size:
        data = s.recv(1024)
        print('receiving')
        total_recv += len(data)
        f.write(data)
        print('writing')
    print('Download Complete!')


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_FILE\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    done = False
    # loop until user requested to exit
    while not done:
        request = input("Enter command: ").upper()
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'EXIT':
                done = True
        else:
            print('Please enter one of the available commands above!')

    my_socket.close()


if __name__ == '__main__':
    main()
