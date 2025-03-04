import os

def test_exist(inp_path):
    if os.access(inp_path, os.F_OK):
        print('Path', inp_path, 'exists')
        print(os.path.basename(inp_path))
        print(os.path.dirname(inp_path))
    else: 
        print('Path does not exist')

inp_path = input()
test_exist(inp_path)