def count_lines(name):
    with open(name, 'r') as file:
        count = 0
        for line in file:
            count += 1
        print(count, 'lines.')

name = input('File path: ')
count_lines(name)