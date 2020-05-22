import  os

def seach(path, name):
    for name_of_obj in os.listdir(path):
        if os.path.isdir(path + '/' + name_of_obj):
            seach(path + '/' + name_of_obj, name)
        else:
            if name_of_obj == name:
                print('File: \033[1m{} \033[0m is here: \033[1m{}'.format(name, path))
                os.system('xdg-open ' + path)
                break

path = '/home/ser_yk/Загрузки'
name = 'CODE_-_Charlz_Pettsold.pdf'

seach(path, name)
