def uplowcase(s):
    up = 0
    low = 0
    for c in s:
        if c.isupper():
            up += 1
        if c.islower():
            low += 1
    print('Lowercase', low)
    print('Uppercase', up)
s = input()
res = uplowcase(s)