
def calculate_next(param):
    for char in str(param):
        if char.isalpha(): # if client entered a letter, return error
            return 'Error: Please enter a number'
    n_param = int(param) + 1
    return str(n_param)


def calculate_area(params):
    params = str(params)
    #Parser to get height and width:
    height = params.split('=', 1)[1]
    height = height[:1]
    params = params.split('&', 1)[1]
    width = params.split('=', 1)[1]
    for c in width:
        if c.isalpha():
            return 'Error: Please enter valid numbers'
    for c in height:
        if c.isalpha():
            return 'Error: Please enter valid numbers'

    return str((int(width) * int(height))/2)

