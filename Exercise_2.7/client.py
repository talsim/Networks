import socket

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
    length = str(len(request)).zfill(2) # add zero to the start of the number if it is one digit
    full_request = length + request # building the request
    my_socket.send(full_request.encode())


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    command = request.rsplit()[0]
    if command == 'SEND_FILE':
        f = open(request.rsplit()[1] + '_RECV', 'wb')
        l = my_socket.recv(1024)
        print('reciving')
        while l:
            f.write(l)
            print('writing')
            l = my_socket.recv(1024)
        f.close()
        print('done')
    data = my_socket.recv(1024)
    print(f'Server sent: {data.decode()}')

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