__author__ = 'Existanza'

import sqlite3


def old_db():
    f = open("C:/pyton/ppeval/osu.txt", "w")
    conn = sqlite3.connect('taikopersonal2015.db')
    c = conn.cursor()
    print('jaka piekna baza danych:')
    i = 0
    for row in c.execute('''SELECT * FROM maps ORDER BY score'''):
        print(row)
        f.write(str(row)+'\n')
        i += 1
    print(i)
    conn.close()
    f.close()


def new_db():
    conn = sqlite3.connect('taikopersonal2015.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE maps (map_id integer, map_name text, diff_name text, last_update text, stars real,
                                    score real, mode text, bpm integer, hit_length integer, user_score real)''')
    conn.commit()
    conn.close()


old_db()
# new_db()
