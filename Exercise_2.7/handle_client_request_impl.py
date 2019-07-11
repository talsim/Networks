
# request_list[0] = command
# request_list[1 ++] = params


def DIR(param):
    from os import listdir
    files_list = listdir(param)
    return files_list

def SEND_FILE(param, s):
    import socket
    f = open(param, 'rb')
    l = f.read(1024)
    print('reading')
    while l:
        print('sending')
        s.send(l)
        l = f.read(1024)
    f.close()
    print('done')
    return 'File has been successfully sended'

def TAKE_SCREENSHOT(param):
    pass

def DELETE(param):
    pass


def COPY(param1, param2):
    pass


def EXECUTE(param):
   pass


