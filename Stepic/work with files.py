import  os, shutil, os.path
lst = []
with open('.\write.txt', 'a') as note:
    for root_dir, dirs, files in os.walk('.\main'):
        for file in files:
            if '.py' in file:
                lst.append(root_dir)
                break
    for dir in sorted(lst):
        note.write(dir[2:] + '\n')