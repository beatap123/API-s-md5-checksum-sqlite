import os

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = """INSERT INTO projects (filename, path, md5sum)
            VALUES (?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def main():
    WORK_DIR = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(WORK_DIR, "pythonsqlite.db")

    sql_create_projects_table = '''CREATE TABLE IF NOT EXISTS projects (
                                    id integer PRIMARY KEY,
                                    filename text NOT NULL,
                                    path text,
                                    md5sum text
                                    );'''

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
