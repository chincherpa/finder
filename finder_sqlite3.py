# -*- coding: utf-8 -*-
import os
import re
import sys
from threading import Thread
import sqlite3
import crayons

this_path = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(this_path, 'myfiles.db')

conn = sqlite3.connect(db_file)
c = conn.cursor()

try:
    print('checking for db_file')
    c.execute('''CREATE TABLE my_files(filename, path)''')
except sqlite3.OperationalError:
    print('db already exists')


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
    print(f'{crayons.blue("searching...")}\n')
    for root, _, files in os.walk(drive, topdown = True):
        root = root.replace(':', ':\\')
    for file in files:
        file = file.lower()
        # pathx = ''.join((root, file))
        file_path = os.path.join(root, file)
        # print(file, pathx)
        entities = (file, file_path)
        # c.execute('''INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)''', entities)
        c.execute('''INSERT INTO my_files (filename, path) VALUES (?, ?)''', entities)


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
        # disregard drive C:
        if drive =='C:':
            continue
        process1 = Thread(target=index, args=(drive,))
        process1.start()


def del_db():
    pass

def show():
    print('show...')


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
