def copy_file(file1, file2):
    with open(file1, 'r') as f1:
        content = f1.read()
    with open(file2, 'a') as f2:
        f2.write(content)
    with open(file2, 'r') as f2:
        print(f2.read())

file1 = input('File 1 path:')
file2 = input('File 2 path:')
copy_file(file1, file2)