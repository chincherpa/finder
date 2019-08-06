# -*- coding: utf-8 -*-
import os
import re
import sys
from threading import Thread
# import subprocess
import json
import crayons



data_dic = {}
this_path = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(this_path, 'finder_data.json')

def get_drives():
    response = os.popen('wmic logicaldisk get caption')
    list1 = []
    for line in response.readlines():
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.strip(' ')
        if (line == 'Caption' or line == ''):
            continue
        list1.append(line)
    return list1


def index(drive: str):
    print(f'{crayons.blue("searching...")} {drive}\n')
    for root, _, files in os.walk(drive, topdown = True):
        root = root.replace(':', ':\\')
        for file in files:
            file = file.lower()
            if file in data_dic:
                file2 = ''.join([file, '_1'])
                data_dic[file2] = os.path.join(root, file)
            else :
                data_dic[file] = os.path.join(root, file)
    return data_dic


def create():
    drives = input('Which drives (A, C, D or (None=all))?\t') or 0
    try:
        with open(data_file, 'r') as fp:
            file_dict = json.load(fp)
    except FileNotFoundError:
        print(f'{crayons.yellow("[INFO] No data found", bold=True)}')
        print(f'{crayons.yellow("[INFO] Will be created...", bold=True)}')
        file_dict = {}
    print('creating...')
    if drives:
        drives_input = drives.replace(' ', '').split(',')
        drives_list = [d + ':' for d in drives_input]
    else:
        drives_list = get_drives()

    print(drives_list)
    list2 = []
    for drive in drives_list:
        if drive =='C:':
            continue
        process1 = Thread(target=index, args=(drive,))
        process1.start()
        list2.append(process1)
          
    for t in list2:
        t.join() # Terminate the threads

    data_dic.update(file_dict)

    with open(data_file, 'w') as fp:
        json.dump(data_dic, fp, sort_keys=True, indent=4)


def del_db():
    if os.path.isfile(data_file):
        print('deleting datbase...')
        os.remove(data_file)
        create()
    else:
        print('no datbase found!\ndo nothing')


def show():
    print('show...')
    if not os.path.isfile(data_file):
        create()
    
    with open(data_file, 'r') as fp:
        finder_dict = json.load(fp)
    print('\nThis is the finder-dict:\n')
    for file, path in finder_dict.items():
        print(f'{file}\t\t{path}')


def find_file():
    if not os.path.isfile(data_file):
        print(crayons.red('no database!', bold=True))
        sys.exit()

    file_to_find = input('Filename:\t') or 0
    if file_to_find:
        with open(data_file, 'r') as fp:
            file_dict = json.load(fp)
        list1= []
        print('#   Filename')
        for key in file_dict:
            if re.search(file_to_find, key):
                list1.append(f'{key}\t\t{file_dict[key]}')
        list1.sort()
        for i, elem in enumerate(list1, 1):
            print(f'{i}   {elem}')
            # print('-' * 40)
        print(f'\n{len(list1)} files found\n')
    else:
        sys.exit()


if __name__ == '__main__':
    print('FIND MY FILES\n')

    while True:
        print('-'*31)
        print('| [F]IND FILE\t\t-  f  ', '|', sep='')
        print('| [A]dd drive to index\t-  a  ', '|', sep='')
        print('| [S]how index\t\t-  s  ', '|', sep='')
        print('| [D]elete index\t-  d  ', '|', sep='')
        print('|', '-'*29, '|', sep='')
        print('| \t\t CANCEL -  c  ', '|', sep='')
        print('-'*31)

        task = input('Your choice?\t')

        if task.lower() == 'a':
            create()
        elif task.lower() == 'f':
            find_file()
        elif task.lower() == 's':
            show()
        elif task.lower() == 'd':
            del_db()
        elif task.lower() == 'c':
            sys.exit()
        else:
            print('Falscher input')
            sys.exit()
