import os.path


# request_list[0] = command
# request_list[1 ++] = params


def validate_DIR(request_list):  # DIR gets the directory to show
    if request_list[1] != None:
        if os.path.isdir(request_list[1]):
            return True
        else:
            return [False, 'directory does not exist!']
    else:
        return [False, 'Please add the directory']


def validate_SEND_FILE(request_list):  # SEND_FILE gets the name of the file to send
    if request_list[1] != None:
        if os.path.isfile(request_list[1]):
            return True
        else:
            return [False, 'File does not exist!']
    else:
        return [False, 'Please add the name of the file']


def validate_DELETE(request_list):  # DELETE gets the name of the file to remove
    if request_list[1] != None:
        if os.path.isfile(request_list[1]):
            return True
        else:
            return [False, 'File does not exist']
    else:
        return [False, 'Please add the name of the file']


def validate_COPY(request_list):  # COPY gets the files to be copied
    if request_list[1] != None:
        if len(request_list) > 2:  # user can enter one param
            param2 = os.getcwd() + '\\' + request_list[2]
            print(f'request_list[1] = {request_list[1]} \nparam2 = {param2}')
            if os.path.isfile(request_list[1]) and os.path.isfile(param2):
                return True
            else:
                return [False, 'one of the files does not exist!']
        else:
            return [False, 'Please add the second parameter']
    else:
        return [False, 'Please add the filed to be copied']


def validate_EXECUTE(request_list):  # EXECUTE gets the file to execute
    if request_list[1] != None:
        if os.path.isfile(request_list[1]):
            return True
        else:
            return [False, 'File does not exist!']
    else:
        return [False, 'Please add the name of the file']
