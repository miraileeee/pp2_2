import os

path = input()
dirlist = os.listdir(path)
print('Files and directories in ', path, ': ')
print(dirlist)