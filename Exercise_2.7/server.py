import socket
from PIL import ImageGrab
import os.path

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


def check_client_request(requestList):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    command = requestList[0]
    try:
        param = os.getcwd() + '\\' + requestList[1]
    except TypeError:
        param = None

    print('param = ' + str(param))
    if command == 'TAKE_SCREENSHOT': # TAKE_SCREENSHOT doesn't get any params
        return [True, None]
    elif command == 'DIR': # DIR gets the directory to show
        if param != None:
            if os.path.isdir(param):
                return [True, None]
            else:
                return [False, 'directory does not exist!']
        else:
            return [False, 'Please add the directory']
    elif command == 'SEND_FILE': # SEND_FILE gets the name of the file to send
        if param != None:
            if os.path.isfile(param):
                return [True, None]
            else:
                return [False, 'File does not exist!']
        else:
            return [False, 'Please add the name of the file']
    elif command == 'DELETE': # DELETE gets the name of the file to remove
        if param != None:
            if os.path.isfile(param):
                return [True, None]
            else:
                return [False, 'File does not exist']
        else:
            return [False, 'Please add the name of the file']
    elif command == 'COPY': # COPY gets the files to be copied
        try: # user can enter one param
            if param != None and requestList[2] != None:
                param2 = os.getcwd() + '\\' + requestList[2]
                if os.path.isfile(param) and os.path.isfile(param2):
                    return [True, None]
                else:
                    return [False, 'one of the files does not exist!']
            else:
                return [False, 'Please add the files to be copied']
        except IndexError:
            return [False, 'Please add the second parameter']

    elif command == 'EXECUTE': # EXECUTE gets the file to execute
        if param != None:
            if os.path.isfile(param):
                return [True, None]
            else:
                return [False, 'File does not exist!']
        else:
            return [False, 'Please add the name of the file']
    else: # command = 'EXIT'
        return [True, None]


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
    listString[0] = listString[0].upper()
    if len(listString) < 2: # if user didn't enter any params
        listString.append(None) # appending None to params
    return listString

#requestList[0] = command
#requestList[1 ++] = params
def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        requestList = receive_client_request(client_socket)
        #print('command = ' + str(requestList[0]) + '\nparams[1] = ' + str(requestList[1])) #+ '\nparams[2] = ' + str(requestList[2])
        valid, error_msg = check_client_request(requestList)
        print('valid = ' + str(valid) + '\nerror_msg = ' + str(error_msg))
        """if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(error_msg, client_socket)"""

        if requestList[0] == 'EXIT':
            print('Quiting')
            done = True

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()