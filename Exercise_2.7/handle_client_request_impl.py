from os import listdir


# request_list[0] = command
# request_list[1 ++] = params


def DIR(param):
    files_list = listdir(param)
    return files_list

def SEND_FILE(param):
    f = open(param, 'rb')
    return f

def TAKE_SCREENSHOT(param):
    pass

def DELETE(param):
    pass


def COPY(param1, param2):
    pass


def EXECUTE(param):
   pass


