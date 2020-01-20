d = {'a':1, 'b':2}

try:
    print(d['x'])
except KeyError:
    print('x is not found')
finally:
    print('post-proccesing')
