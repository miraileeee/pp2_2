import os

def delete_file(path):
    if os.access(path, os.F_OK):
        print('Path', path, 'exists')
        os.remove(path)
    else: 
        print('Path does not exist')

path = input('File path: ')
delete_file(path)