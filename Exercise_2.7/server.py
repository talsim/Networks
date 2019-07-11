import socket
from PIL import ImageGrab
import os.path


IP = '0.0.0.0'
PORT = 8820
#request_list[0] = command
#request_list[1 ++] = params


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


def check_client_request(request_list):
    """Check if the params are good.
    For example, the filename to be copied actually exists
    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """

    command = request_list[0]
    if request_list[1] != None:
        request_list[1] = os.getcwd() + '\\' + request_list[1]
    else:
        request_list[1] = None
    print(f'request_list = {request_list}')
    if command == 'TAKE_SCREENSHOT':
        return True
    elif command == 'EXIT': # command == 'EXIT'
        return True
    import param_validators
    return getattr(param_validators, f'validate_{command}')(request_list)


def handle_client_request(request_list):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    return 'data you wanted'
	

def send_response_to_client(response, client_socket, command = None):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    if command is None: # if respone = error_msg
        client_socket.send(str(response).encode())
    else:
        client_socket.send(str(response).encode())


def my_split(string):
    list_string = string.split()
    list_string[0] = list_string[0].upper()
    if len(list_string) < 2:  # if user didn't enter any params
        list_string.append(None)  # appending None to params
    return list_string


#validation_list[0] = valid (True/False)
#validation_list[1] = error_msg (if valid is False)
def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    # handle requests until user asks to exit
    done = False
    while not done:
        request_list = receive_client_request(client_socket)
        validation_list = check_client_request(request_list)
        if validation_list == True: # if valid is True
            response = handle_client_request(request_list)
            send_response_to_client(response, client_socket, request_list[0])
        else:
            send_response_to_client(validation_list[1], client_socket)

        if request_list[0] == 'EXIT':
            print('Quiting')
            done = True

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()