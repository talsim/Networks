import os
from pathlib import Path


def calculate_next(param):
    if is_valid_string(str(param)):
        param = param[0]
        n_param = int(param) + 1
        return str(n_param)
    return 'Error: Please enter a number'


def calculate_area(params):
    params = params[0]
    width, height = calc_area_parser(params)
    if is_valid_string(width) and is_valid_string(height):
        return str((int(width) * int(height)) / 2)
    return 'Error: Please enter valid numbers'


def upload(params_list):
    name = params_list[0]
    client = params_list[1]
    req = params_list[2]
    size = req.split(b'Content-Length: ')[1].split(b'\r\n')[0]  # getting the size of the image
    rest_data = req.split(b'\r\n\r\n')[1]  # rest of data after the header
    chunk = 20000  # chunk to recv every time
    data = rest_data + client.recv(chunk)
    total_recv = len(data)
    path = build_path('uploads', name)
    with open(path, 'wb') as f:
        f.write(data)
        while total_recv < int(size):
            data = client.recv(chunk)
            print('receiving')
            total_recv += len(data)
            f.write(data)
            print('writing')
        print('Download Complete')
    return 'File has uploaded successfully!'


def image(params_list):
    name = params_list[0]
    client = params_list[1]
    path = build_path('uploads', name)
    if os.path.isfile(path):
        img = open(path, 'rb')
        data = img.read()
        client.sendall(data)
    return 'Error: The file does not exist'


def calc_area_parser(param):
    param = str(param)
    height = param.split('height=', 1)[1].split('&width', 1)[0]
    width = param.split('width=', 1)[1]
    return [width, height]


def is_valid_string(s):
    for c in s:
        if c.isalpha():
            return False
    return True


def build_path(folder, name):
    """
    Function for building path to root
    """
    folder = Path(folder)
    name = Path(name)
    root = f'{os.getcwd()}{os.sep}webroot'
    directory = folder / name
    full_path = root / directory
    return full_path
