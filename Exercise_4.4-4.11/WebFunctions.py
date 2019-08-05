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


def upload(param):
    pass


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
