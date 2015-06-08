__author__ = 'Existanza'

import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
print('jaka piekna baza danych:')
for row in c.execute('''SELECT * FROM maps ORDER BY score'''):
    print(row)
conn.close()