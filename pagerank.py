import sqlite3
import numpy as np

'''
page_rank(ith iteration) = sum( pr_i-1th iteration of all nodes pointing to  )
'''

connection = sqlite3.connect("spider_database.sqlite")
cur = connection.cursor()

cur.execute("SELECT from_page_id, to_page_id FROM Links")

rows = cur.fetchall()

# store all the links that a current link points to 
outbound_links = {}

# store all the links that point to a current link
inbound_links = {}

maxx = 0

for row in rows:
    # if the page links to itself, then don't consider that
    if row[0] == row[1]:
        continue

    # lst.append(row)
    if row[0] not in outbound_links:
        outbound_links[row[0]] = []

    outbound_links[row[0]].append(row[1])

    max_of_rows = max(row[0], row[1])

    if max_of_rows > maxx:
        maxx = max_of_rows

adjacency_mat = np.zeros((maxx, maxx))

for _id in outbound_links:
    page_id = outbound_links.get(_id)
    for i in range(len(page_id)):

        from_page = _id
        to_page = page_id[i]

        adjacency_mat[to_page - 1][from_page - 1] = 1

print(outbound_links, maxx, "\n" ,adjacency_mat)





