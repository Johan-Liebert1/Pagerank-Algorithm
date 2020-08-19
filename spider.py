import sqlite3
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = sqlite3.connect('spider_database.sqlite')
cur = connection.cursor()


cur.executescript('''
    CREATE TABLE IF NOT EXISTS Websites (
        website TEXT 
    );

    CREATE TABLE IF NOT EXISTS Pages (
        id INTEGER NOT NULL PRIMARY KEY,
        url TEXT UNIQUE, 
        html TEXT, 
        error INTEGER DEFAULT NULL,
        old_rank REAL,
        new_rank REAL
    );

    CREATE TABLE IF NOT EXISTS Links (
        from_page_id INTEGER, 
        to_page_id INTEGER,

        UNIQUE (from_page_id, to_page_id)
    )
''')