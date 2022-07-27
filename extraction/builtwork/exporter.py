from ast import Try
from calendar import c
import psycopg2
import os
from configparser import ConfigParser

curr_dir = os.path.dirname(os.path.realpath(__file__))

def config(filename=os.path.join(curr_dir, 'database.ini'), section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    db = {}

    try:
      params = parser.items(section)
      for param in params:
          db[param[0]] = param[1]

    except Exception as e:
      print(e)

    return db

def connect():
  """ Connect to the PostgreSQL database server """
  conn = None
  try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()
      
    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
      
    # close the communication with the PostgreSQL
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()
      print('Database connection closed.')

if __name__ == '__main__':
    connect()