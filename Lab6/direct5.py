def write_file(inp, name):
    with open(name, 'w') as file:
        file.write('\n'.join(inp))
        file.close()
    with open(name, 'r') as file:
        print(file.read())

inp = input().split()
name = input('File path: ')
write_file(inp, name)