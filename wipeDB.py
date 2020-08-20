import sqlite3

conn = sqlite3.connect("spider_database.sqlite")
cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS Pages;
    DROP TABLE IF EXISTS Websites;
    DROP TABLE IF EXISTS Links;
""")

conn.commit()

print("ALL TABLES DELETED")

cur.close()
