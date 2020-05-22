offset, string = (input() for i in (1,2))
alf = ' abcdefghijklmnopqrstuvwxyz'
new_string = ''

for char in string.strip():
    new_string = new_string + str(alf[(alf.index(char) + int(offset)) % 27])

print(f'Result: "{new_string}"')