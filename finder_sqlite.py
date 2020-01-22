import os
import sqlite3
import time

import crayons
from halo import Halo
spinner = Halo(text='working...', spinner='dots')


dir_path = os.path.dirname(os.path.realpath(__file__))
db_name = 'my_db.db'
path_to_db = os.path.join(dir_path, db_name)

# os.chdir(dir_to_read)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:  # Error as e:
        print("Error")


if not os.path.isfile(path_to_db):
    print('not os.path.isfile(path_to_db)')
    open(db_name, 'a').close()

conn = create_connection(path_to_db)
c = conn.cursor()

try:
    c.execute('CREATE TABLE my_files(filename, path)')
except sqlite3.OperationalError as e:
    print(crayons.yellow('\n[INFO]', bold=True), e)


def remove_path(folder: str):
    c.execute('DELETE FROM my_files WHERE path LIKE ?', (f'%{folder}%',))


def index(le_dir: str):
    time_start = time.time()

    print('updating entries...\n')
    spinner.start()
    remove_path(le_dir)
    for root, _, files in os.walk(le_dir, topdown=True):
        # root = root.replace(':', ':/')
        for file in files:
            entities = (file.lower(), root)  # os.path.join(root, file.lower()))
            c.execute('''INSERT INTO my_files (filename, path) VALUES (?, ?)''', entities)
    conn.commit()
    print('\n',
          crayons.yellow('Successfully tried to add'),
          crayons.blue(f'{le_dir}'),
          crayons.yellow('to the index.'))
    spinner.stop()
    dur = time.time() - time_start
    print(crayons.yellow('\nTook:'), crayons.yellow(time.strftime('%H:%M:%S', time.gmtime(dur))))


def find_item(item: str, file_: bool = True) -> list:
    spinner.start()
    global time_start
    time_start = time.time()
    # find file
    if file_:
        print('Looking for entries (files)...\n')
        c.execute('SELECT * FROM my_files WHERE filename LIKE ?', (f'%{item}%',))
        found_items = c.fetchall()
    # find folder
    else:
        print('Looking for entries (folders)...\n')
        c.execute('SELECT * FROM my_files WHERE path LIKE ?', (f'%{item}%',))
        all_items = c.fetchall()
        found_items = []
        found_paths = []
        for f, p in all_items:
            if p not in found_paths:
                found_paths.append(p)
                found_items.append([f, p])

    spinner.stop()
    return found_items


def find_item_in_folder(file_: str, folder: str) -> list:
    print('\nLooking for files with "', crayons.yellow(file_), '" in name\nin folder ', crayons.green(folder), '\n', sep='')
    spinner.start()
    global time_start
    time_start = time.time()
    # find file
    c.execute("SELECT * FROM my_files WHERE filename LIKE ? AND path Like ?", ('%' + file_ + '%', folder + '%',))
    found_items = c.fetchall()

    spinner.stop()
    return found_items


def show_folder(path: str) -> list:
    spinner.start()
    global time_start
    time_start = time.time()
    # find file
    print('Looking for entries (folders)...\n')
    c.execute('SELECT * FROM my_files WHERE path LIKE ?', (f'%{path}%',))

    found_items = c.fetchall()

    spinner.stop()
    return found_items


def show_found(list_found: list) -> None:
    for i, f in enumerate(list_found):
        print(crayons.yellow(i), crayons.yellow(f' {f[0]}', bold=True), '\t<|>  ', f'{f[1]}', sep='')
        # print(crayons.yellow(f'\n{num.fetchone()[0]}'), 'entries in db.')
    dur = time.time() - time_start
    print(crayons.yellow('\nTook:'), crayons.yellow(time.strftime('%H:%M:%S', time.gmtime(dur))))


def count_entries():
    spinner.start()
    num = c.execute('SELECT COUNT(*) FROM my_files')
    print(crayons.yellow(f'\n{num.fetchone()[0]}'), 'entries in db.')
    spinner.stop()


while True:
    print('\n')
    print(crayons.BLUE('#' * 55, bold=True))
    print(crayons.BLUE('#' * 20, bold=True), crayons.BLUE('FIND MY FILES', bold=True), crayons.BLUE('#' * 20, bold=True))
    print(crayons.BLUE('#' * 55, bold=True), '\n')
    print(crayons.YELLOW('-' * 33))
    print(crayons.YELLOW('|'), 'FIND [', crayons.MAGENTA('F', bold=True), ']ILE\t\t\t', crayons.YELLOW('|'), "\t# or 'f part of FILENAME'", sep='')
    print(crayons.YELLOW('|'), 'FIND [', crayons.MAGENTA('FF', bold=True), ']ILE in FOLDER\t\t', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('|'), 'FIND [', crayons.MAGENTA('FO', bold=True), ']LDER\t\t\t', crayons.YELLOW('|'), "\t# or 'fo part of PATH'", sep='')
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('S', bold=True), ']how folder\t\t\t', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('-' * 33))
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('A', bold=True), ']dd path to index\t\t', crayons.YELLOW('|'), "\t# or 'a PATH'", sep='')
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('R', bold=True), ']emove path from index\t', crayons.YELLOW('|'), "\t# or 'r PATH'", sep='')
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('SX', bold=True), ']how index\t\t\t', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('NX', bold=True), ']umber of entries\t\t', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('|'), '[', crayons.MAGENTA('DX', bold=True), ']elete index\t\t', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('|'), crayons.YELLOW('-' * 31), crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('|'), '\t\t\t[', crayons.MAGENTA('C', bold=True), ']ANCEL', crayons.YELLOW('|'), sep='')
    print(crayons.YELLOW('-' * 33))

    task = input('Your choice?\t')

    # shortcut find file
    if task[:3].lower() == 'fo ':
        folder = task[3:]
        findings = find_item(folder, False)
        show_found(findings)
    # find file in a specific folder
    elif task[:2].lower() == 'ff':
        file_ = input('File to look for...:\t') or 0
        if file_:
            folder = input('...in folder:\t') or 0
            if folder:
                findings = find_item_in_folder(file_, folder)
                show_found(findings)
    # shortcut find file
    elif task[:2].lower() == 'f ':
        file_ = task[2:]
        findings = find_item(file_)
        show_found(findings)
    # shortcut add path
    elif task[:2].lower() == 'a ':
        dir_to_read = task[2:]
        index(dir_to_read)
    # shortcut remove path
    elif task[:2].lower() == 'r ':
        dir_to_remove = task[2:]
        remove_path(dir_to_remove)
    # shortcut show folder
    elif task[:2].lower() == 's ':
        dir_to_show = task[2:]
        findings = show_folder(dir_to_show)
        show_found(findings)
    elif task.lower() == 'f':
        file_ = input('File to look for:\t') or 0
        if file_:
            print(f'Looking for FILES with "{file_}" in name...')
            findings = find_item(file_, True)
            show_found(findings)
        else:
            print('no input')
    elif task.lower() == 'fo':
        folder = input('Folder to look for:\t') or 0
        if folder:
            print(f'Looking for FOLDERS with "{folder}" in path...')
            findings = find_item(folder, False)
            show_found(findings)
        else:
            print('no input')
    elif task.lower() == 'a':
        dir_to_read = input('Directory:\t') or 0
        if dir_to_read:
            index(dir_to_read)
    elif task.lower() == 'r':
        dir_to_remove = input('Directory:\t') or 0
        if dir_to_remove:
            remove_path(dir_to_remove)
    elif task.lower() == 's':
        folder = input('Folder to show:\t') or 0
        if folder:
            findings = show_folder(folder)
            show_found(findings)
    elif task.lower() == 'n':
        count_entries()
    elif task.lower() == 'd':
        print('del_db()')
    elif task.lower() == 'c':
        print('\nclosing connection...\n')
        # conn.close()
        break
    else:
        pass
        # print('Falscher input')


print('done')
