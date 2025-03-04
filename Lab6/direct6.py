def atoz_file(inp, name):
    for i in range(26):
        name = chr(65 + i) +'.txt'

        with open(name, 'w') as file:
            file.write(chr(65 + i))
        with open(name, 'r') as file:
            print(file.read())

atoz_file()