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
    if query.lower() == "all":
        cur.execute("SELECT * FROM Tweet")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        
    elif "last " in query.lower():
        num = int(query.split(" ")[1])
        q = "SELECT * FROM Tweet ORDER BY created_at LIMIT {};".format(num)
        cur.execute(q)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    elif "info" in query.lower():
        q1 = "SELECT count(Tweet.id) FROM Tweet;"
        q2 = "SELECT count(Place.id) FROM Place;"
        q3 = "SELECT count(User.id) FROM User;"
        cur.execute(q1)
        row1 = cur.fetchone()[0]
        cur.execute(q2)
        row2 = cur.fetchone()[0]
        cur.execute(q3)
        row3 = cur.fetchone()[0]
        print("Tweet: {}  Place: {}  User: {}".format(row1, row2, row3))

    else:
        cur.execute(query)
        rows = cur.fetchall()
        #for row in rows:
        #    print(row)
        return rows
            

def run():
    # create a database connection
    conn = get_db()
    print("Table = 'Tweet', 'Place', 'User'\nPremade queries: info, all, last <num>")
    query_db(conn, "info")
    while True:
        try:
            user_inp = input("Query> ")
            print("\n")
            query_db(conn, user_inp)
            print("\n")
        except Exception as e:
            pass