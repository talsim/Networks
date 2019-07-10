import os.path


#request_list[0] = command
#request_list[1 ++] = params


def validate_DIR(request_list):
    if request_list[0] == 'DIR': # DIR gets the directory to show
        if request_list[1] != None:
            if os.path.isdir(request_list[1]):
                return True
            else:
                return [False, 'directory does not exist!']
        else:
            return [False, 'Please add the directory']


def validate_SEND_FILE(request_list):
    if request_list[0] == 'SEND_FILE': # SEND_FILE gets the name of the file to send
        if request_list[1] != None:
            if os.path.isfile(request_list[1]):
                return True
            else:
                return [False, 'File does not exist!']
        else:
            return [False, 'Please add the name of the file']


def validate_DELETE(request_list):
    if request_list[0] == 'DELETE':  # DELETE gets the name of the file to remove
        if request_list[1] != None:
            if os.path.isfile(request_list[1]):
                return True
            else:
                return [False, 'File does not exist']
        else:
            return [False, 'Please add the name of the file']


def validate_COPY(request_list):
    if request_list[0] == 'COPY': # COPY gets the files to be copied
        try: # user can enter one param
            if request_list[1] != None and request_list[2] != None:
                param2 = os.getcwd() + '\\' + request_list[2]
                if os.path.isfile(request_list[1]) and os.path.isfile(param2):
                    return True
                else:
                    return [False, 'one of the files does not exist!']
            else:
                return [False, 'Please add the files to be copied']
        except IndexError:
            return [False, 'Please add the second parameter']


def validate_EXECUTE(request_list):
    if request_list[0] == 'EXECUTE': # EXECUTE gets the file to execute
        if request_list[1] != None:
            if os.path.isfile(request_list[1]):
                return True
            else:
                return [False, 'File does not exist!']
        else:
            return [False, 'Please add the name of the file']


