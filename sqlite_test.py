import sqlite3
import os

os.chdir("A:\\sqlite_db")

print('1')
conn = sqlite3.connect('myfiles.db')
print('2')
c = conn.cursor()
try:
    print('3')
    c.execute('''CREATE TABLE my_files(filename, path)''')
except sqlite3.OperationalError:
    print('db already exists')

print('4')
for root, _, files in os.walk('A:', topdown = True):
    root = root.replace(':', ':\\')
    for file in files:
        file = file.lower()
        # pathx = ''.join((root, file))
        file_path = os.path.join(root, file)
        # print(file, pathx)
        entities = (file, file_path)
        # c.execute('''INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)''', entities)
        c.execute('''INSERT INTO my_files (filename, path) VALUES (?, ?)''', entities)

print('5')
conn.commit()
print('6')
conn.close()
print('ENDE')


# import sqlite3
# con = sqlite3.connect('mydatabase.db')
# def sql_insert(con, entities):
    # cursorObj = con.cursor()
    # cursorObj.execute('INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)', entities)
    # con.commit()
# entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
# sql_insert(con, entities)