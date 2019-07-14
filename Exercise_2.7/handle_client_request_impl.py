from os import listdir
from PIL import ImageGrab

# request_list[0] = command
# request_list[1 ++] = params


def DIR(request_list):
    files_list = listdir(request_list[1])
    return files_list

def SEND_FILE(request_list):
    f = open(request_list[1], 'rb')
    return f

def TAKE_SCREENSHOT(request_list):
    im = ImageGrab.grab()
    im.save('screenshot_to_send.png')
    return im

def DELETE(request_list):
    pass


def COPY(request_list):
    pass


def EXECUTE(request_list):
   pass


