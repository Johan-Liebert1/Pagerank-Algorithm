import sqlite3

conn = sqlite3.connect('spider_database.sqlite')
cur = conn.cursor()

cur.execute("""
    UPDATE Pages 
    SET old_rank = NULL, new_rank = 1.0
""")

conn.commit()

cur.close()