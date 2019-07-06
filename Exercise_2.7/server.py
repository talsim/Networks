import socket
from PIL import ImageGrab

IP = '0.0.0.0'
PORT = 8820


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    recvsize = client_socket.recv(2) # length of the request
    request = client_socket.recv(int(recvsize.decode())) # the request
    return my_split(request.decode()) # splitting the request to command and params


def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    pass


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    pass


def send_response_to_client(response, client_socket):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    client_socket.send(response)
    pass

def my_split(string):
    listString = string.split()
    if len(listString) < 2: # if user didn't enter any params
        listString.append(None) # appending None to params
    return listString

def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        print('command = ' + command + '\nparams = ' + str(params))
        """valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(error_msg, client_socket)"""

        if command == 'EXIT':
            print('Quiting')
            done = True

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()