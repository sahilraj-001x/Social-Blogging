import sqlite3
import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath(__file__))

def create_newusers(username, password, email, age):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('insert into newusers (username,password,email,age) values(? ,? ,?, ?)', (username, password, email, age))
    con.commit()
    con.close()

def posts(auther , title , post):
    connection = sql.connect(path.join(ROOT, "postss.db"))
    curser = connection.cursor()
    curser.execute("INSERT INTO data (auther , title , post) values(? ,? ,?)", (auther , title , post))
    connection.commit()
    connection.close()

# connect = sql.connect('comments.db')
# crsr = connect.cursor()
#
# crsr.execute("""CREATE TABLE comments(
#         title VARCHAR(50) NOT NULL,
#         comment1 VARCHAR(50) NOT NULL,
#         comment2 VARCHAR(50) NOT NULL,
#         comment3 VARCHAR(50) NOT NULL,
#         comment4 VARCHAR(50) NOT NULL,
#         comment5 VARCHAR(50) NOT NULL,
#         comment6 VARCHAR(50) NOT NULL,
#         comment7 VARCHAR(50) NOT NULL,
#         comment8 VARCHAR(50) NOT NULL,
#         comment9 VARCHAR(50) NOT NULL,
#         comment10 VARCHAR(50) NOT NULL
# )""")
#
# connect.commit()
# connect.close()


# con = sql.connect('database.db')
# cur = con.cursor()
#
# cur.execute("""CREATE TABLE newusers(
#         username VARCHAR(30) NOT NULL,
#         password VARCHAR(20) NOT NULL,
#         email VARCHAR(30) NOT NULL,
#         age INTEGER NOT NULL
# )""")
# con.commit()
# con.close()