import sqlite3, sys
from termcolor import colored

conn = sqlite3.connect("spider_database.sqlite")
cur = conn.cursor()

print(colored("WARNING, ALL TABLES WILL BE DELETED!", 'red'))
cont = input('Continue? (Y/N) > ')

if cont.lower() == 'y':
    cur.executescript("""
        DROP TABLE IF EXISTS Pages;
        DROP TABLE IF EXISTS Websites;
        DROP TABLE IF EXISTS Links;
    """)

    conn.commit()

    print(colored("ALL TABLES DELETED", 'green'))

    cur.close()

else:
    sys.exit()
