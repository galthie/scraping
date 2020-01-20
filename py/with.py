with open('index.html') as f:
    print(f.read())


f = open('index.html')
try:
    print(f.read())
finally:
    f.close()
