s = input()
table_encrypt = input()

def encrypt_substitution(s, table_encrypt):
    res = ""
    for i in s:
        if i.isalpha():
            if i.islower():
                res += table_encrypt[ord(i) - ord('a')].lower()
            else:
                res += table_encrypt[ord(i) - ord('A')].upper()
        else:
            res += i

    return res

def decrypt_substitution(s, table_encrypt):
    res = ""
    for i in s:
        if i.isalpha():
            if i.islower():
                res += chr(table_encrypt.index(i.upper()) + ord('a'))
            else:
                res += chr(table_encrypt.index(i.upper()) + ord('A'))
        else:
            res += i

    return res

encrypted = encrypt_substitution(s, table_encrypt)
print(encrypted)
decrypted = decrypt_substitution(s, table_encrypt)
print(decrypted)