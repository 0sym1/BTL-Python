s = input()
key = input()

def encrypt(s, key):
    res = ""
    for i in range(len(s)):
        if s[i].isalpha():
            if s[i].islower():
                res += chr((ord(key[i%len(key)].lower()) + ord(s[i]) - 2*ord('a')) % 26 + ord('a'))
            else:
                res += chr((ord(key[i%len(key)].upper()) + ord(s[i]) - 2*ord('A')) % 26 + ord('A'))
            
        else:
            res += s[i]
    
    return res
    
def decrypt(s, key):
    res = ""
    for i in range(len(s)):
        if s[i].isalpha():
            if s[i].islower():
                res += chr((ord(s[i]) - ord(key[i%len(key)].lower()) + 26) % 26 + ord('a'))
            else:
                res += chr((ord(s[i]) - ord(key[i%len(key)].upper()) + 26) % 26 + ord('A'))
        else:
            res += s[i]
    
    return res

encrypted = encrypt(s, key)
print(encrypted)

decrypted = decrypt(s, key)
print(decrypted)