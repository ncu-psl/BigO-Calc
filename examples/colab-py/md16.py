import math
def module16():
    result = []
    for i in dir(math):
        if 'expm' in i:
            result.append(i)
    print(result)