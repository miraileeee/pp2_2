def palindrome(s):
    s1 = s.lower()
    s2 = ''.join(reversed(s1))
    if s1 == s2:
        print('Palindrome')
    else:
        print('Not a palindrome')
s = input()
palindrome(s)