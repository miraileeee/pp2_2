import os

def access_test(path):
    if os.access(path, os.F_OK):
        print('Path', path, 'exists')
        
        if os.access(path, os.R_OK):
            print(path, 'is readable')
        else:
            print(path, 'is not readable')

        if os.access(path, os.W_OK):
            print(path, 'is writable')
        else:
            print(path, 'is not writable')

        if os.access(path, os.X_OK):
            print(path, 'is executable')
        else:
            print(path, 'is not executable')

    else: 
        print('Path does not exist')

path = input()
access_test(path)