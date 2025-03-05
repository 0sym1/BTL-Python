s = input()
k = int(input())

def encrypt_ceasar(s, k):
    res = ""
    for i in s:
        if i.isalpha():
            if i.islower():
                res += chr((ord(i) - ord('a') + k) % 26 + ord('a'))
            else:
                res += chr((ord(i) - ord('A') + k) % 26 + ord('A'))
        else:
            res += i
    return res

encrypted = encrypt_ceasar(s, 3)
print(encrypted)

def decrypt_ceasar(s, k):
    res = ""
    for i in s:
        if i.isalpha():
            if i.islower():
                res += chr((ord(i) - ord('a') - k) % 26 + ord('a'))
            else:
                res += chr((ord(i) - ord('A') - k) % 26 + ord('A'))
        else:
            res += i
    return res

decrypted = decrypt_ceasar(s, k)
print(decrypted)


