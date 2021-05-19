def assym(a, g, p):
    key = g ** a % p
    return key


def valid(key_publ_s):
    try:
        i = False
        file = open("allowed.txt", "r")
        for line in file:
            if line[0] == str(key_publ_s):
                i = True
        return i
    except:
        return False


def encode(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j += key
        j = chr(j)
        s[i] = j

    return ''.join(s)


def decode(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j -= key
        j = chr(j)
        s[i] = j
    return ''.join(s)
