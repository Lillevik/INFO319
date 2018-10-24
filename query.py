#!/usr/bin/python
import sqlite3
from sqlite3 import Error
import os
 
 
def get_db():
    """ create a database connection to the SQLite database
    :return: Connection object or None
    """
    try:
        db_file = "{}/Tweets_db.sqlite".format(os.path.dirname(os.path.realpath(__file__)))
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
 
 
def query_db(conn, query):
    """
    Query all rows in the Tweet table
    :param conn: the Connection object
    """
    cur = conn.cursor()
    rows = None
    if query.lower() == "all":
        cur.execute("SELECT * FROM Tweet")
        rows = cur.fetchall()
        
    elif "last " in query.lower():
        num = int(query.split(" ")[1])
        q = "SELECT * FROM Tweet ORDER BY created_at LIMIT {};".format(num)
        cur.execute(q)
        rows = cur.fetchall()

    else:
        cur.execute(query)
        rows = cur.fetchall()
    
    for row in rows:
        print(row)

def run():
    # create a database connection
    conn = get_db()
    print("Table = 'Tweet'\nPremade queries: all, last <num>")
    while True:
        user_inp = input("Query> ")
        query_db(conn, user_inp)

run()