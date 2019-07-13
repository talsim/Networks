import socket
import os.path
import param_validators
import handle_client_request_impl

IP = '0.0.0.0'
PORT = 8820


# request_list[0] = command
# request_list[1 ++] = params


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    recvsize = client_socket.recv(2)  # length of the request
    request = client_socket.recv(int(recvsize.decode()))  # the request
    return my_split(request.decode())  # splitting the request to command and params


def check_client_request(request_list):
    """Check if the params are good.
    For example, the filename to be copied actually exists
    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """

    command = request_list[0]
    print(f'request_list = {request_list}')
    if request_list[1] != None:
        request_list[1] = os.getcwd() + '\\' + request_list[1]
    if command == 'TAKE_SCREENSHOT' or command == 'EXIT':
        return True
    validator = getattr(param_validators, f'validate_{command}')(request_list)
    print(f'validator = {validator}')
    return validator


def handle_client_request(request_list, c_socket):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    command = request_list[0]

    if command == 'EXIT':
        return 'Quiting'
    elif command == 'COPY':
        response = getattr(handle_client_request_impl, 'COPY')(request_list[1], request_list[2])
        print(f'response = {response}')
        return response
    response = getattr(handle_client_request_impl, command)(request_list[1])
    return response


def send_response_to_client(response, client_socket, command, error = False):
    """Create a protocol which sends the response to the client

    the protocol gets the response and checks if its an error or the data
    and operates according to it
    """
    if error == False:
        if command == 'SEND_FILE':
            client_socket.send(b'sf_sending')
            f = response
            l = f.read(1024)
            print('reading')
            recv = client_socket.recv(1024)
            if recv == 'ready'.encode():
                while l:
                    print('sending')
                    client_socket.send(l)
                    l = f.read(1024)
                    print('reading')
            f.close()
            print('done')
            client_socket.shutdown(socket.SHUT_WR)
            return
        elif command == 'TAKE_SCREENSHOT':
            pass
    client_socket.send(str(response).encode())

def my_split(string):
    list_string = string.split()
    list_string[0] = list_string[0].upper()
    if len(list_string) < 2:  # if user didn't enter any params
        list_string.append(None)  # appending None to params
    return list_string


# validation_list[0] = valid (True/False)
# validation_list[1] = error_msg (if valid is False)
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
        if validation_list is True:  # if valid is True
            response = handle_client_request(request_list, client_socket)
            send_response_to_client(response, client_socket, request_list[0])
        else:
            send_response_to_client(validation_list[1], client_socket, request_list[0], True)

        if request_list[0] == 'EXIT':
            done = True

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
