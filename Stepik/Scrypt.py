import simplecrypt

with open(r'.\temp_files\encrypted.bin', 'rb') as file:
    encrypted = file.read()
    with open(r'.\temp_files\passwords.txt') as password:
        for line in password:
            try:
                print(simplecrypt.decrypt(line.strip(), encrypted), '\n')
                break
            except:
                print('Wrong password!!!')




