import psycopg2

_author_ = 'Existanza'

db_name = 'db6'


def old_db(c):
    f = open("/home/mz/PycharmProjects/osu.txt", "w")
    print('jaka piekna baza danych:')
    i = 0
    c.execute('''SELECT * FROM maps ORDER BY score''')
    rows = c.fetchall()
    for row in rows:
        print(row)
        f.write(str(row)+'\n')
        i += 1
    print(i)
    f.close()


def new_db(c):
    c.execute('''CREATE TABLE maps (map_id integer, map_name text, diff_name text, last_update text, stars real,
                                    score real, mode text, bpm real, hit_length integer, user_score real)''')


def erase_db(c):
    c.execute('''DROP TABLE maps''')


file = open('/home/mz/PycharmProjects/keys/postgres.txt', 'r')
pwd = file.read()
pwd = pwd[:-1]
conn = psycopg2.connect(database=db_name, user='postgres', password=pwd)
c = conn.cursor()

old_db(c)
# new_db(c)
# erase_db(c)

conn.commit()
conn.close()