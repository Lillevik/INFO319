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
 
 
def query_db(conn):
    """
    Query all rows in the Tweet table
    :param conn: the Connection object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tweet")
    rows = cur.fetchall()
    for row in rows:
        print(row)
 
 
def run():
    # create a database connection
    conn = get_db()
    query_db(conn)

run()