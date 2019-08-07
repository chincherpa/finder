import sqlite3
import os

dir_to_read = 'C:\\Users\\x123069\\Desktop'
dir_path = os.path.dirname(os.path.realpath(__file__))
db_name = 'my_db.db'
path_to_db = os.path.join(dir_path, db_name)

os.chdir(dir_to_read)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

if not os.path.isfile(path_to_db):
    open(db_name, 'a').close()

conn = create_connection(path_to_db)
c = conn.cursor()

try:
    c.execute('''CREATE TABLE my_files(filename, path)''')
except sqlite3.OperationalError as e:
    print('[INFO]', e)


def index(dir: str):
    for root, _, files in os.walk(dir, topdown = True):
        root = root.replace(':', ':\\')
        for file in files:
            entities = (file.lower(), os.path.join(root, file.lower()))
            c.execute('''INSERT INTO my_files (filename, path) VALUES (?, ?)''', entities)


def find_file(file: str) -> list:
    c.execute('SELECT * FROM my_files WHERE filename LIKE ?', ('{}%'.format(file),))
    found_files = c.fetchall()
    return found_files


def show_found(list_found: list):
    for i, f in enumerate(list_found):
        print(i, f'\t{f[0]}', f'\t{f[1]}')



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
        index(dir_to_read)
    elif task.lower() == 'f':
        file = input('File to find:\t') or 0
        if file:
            findings = find_file(file)
            show_found(findings)        
    elif task.lower() == 's':
        print('show()')
    elif task.lower() == 'd':
        print('del_db()')
    elif task.lower() == 'c':
        sys.exit()
    else:
        print('Falscher input')


conn.commit()
conn.close()
print('done')
