import os


def calculate_next(param):
    if is_valid_string(str(param)):
        n_param = int(param) + 1
        return str(n_param)
    return 'Error: Please enter a number'


def calculate_area(params):
    width, height = calc_area_parser(params)
    if is_valid_string(width) and is_valid_string(height):
        return str((int(width) * int(height)) / 2)
    return 'Error: Please enter valid numbers'


def upload(file_name, client, req):
    size = req.split(b'Content-Length: ')[1].split(b'\r\n')[0]  # getting the size of the image
    rest_data = req.split(b'\r\n\r\n')[1]  # rest of data after the header
    chunk = 20000  # chunk to recv every time
    data = rest_data + client.recv(chunk)
    total_recv = len(data)
    upload_path = f'{os.getcwd()}{os.sep}webroot{os.sep}uploads{os.sep}{file_name}'
    with open(upload_path, 'wb') as f:
        f.write(data)
        while total_recv < int(size):
            data = client.recv(chunk)
            print('receiving')
            total_recv += len(data)
            f.write(data)
            print('writing')
        print('Download Complete')
    return 'File has uploaded successfully!'


def calc_area_parser(param):
    param = str(param)
    height = param.split('=', 1)[1].split('&', 1)[0]
    param = param.split('&', 1)[1]
    width = param.split('=', 1)[1]
    return [width, height]


def is_valid_string(s):
    for c in s:
        if c.isalpha():
            return False
    return True
