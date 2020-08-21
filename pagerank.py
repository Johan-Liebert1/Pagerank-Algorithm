import sqlite3
import numpy as np
import sys

connection = sqlite3.connect("spider_database.sqlite")
cur = connection.cursor()

cur.execute("SELECT from_page_id, to_page_id FROM Links")

rows = cur.fetchall()

# store all the links that a current link points to 
outbound_links = {}

# store all the links that point to a current link
inbound_links = {}


for row in rows:
    # if the page links to itself, then don't consider that
    if row[0] == row[1]:
        continue

    if row[0] not in outbound_links:
        outbound_links[row[0]] = []

    if row[1] not in inbound_links:
        inbound_links[row[1]] = []

    outbound_links[row[0]].append(row[1])
    inbound_links[row[1]].append(row[0])


# get previous ranks and store them in a list
# 'new_ranks' are the prev_ranks as after this iteration, they'll be 
# moved to the 'old_ranks' column
prev_ranks = {}

for page_id in outbound_links:
    cur.execute("SELECT new_rank FROM Pages WHERE id = ?", (page_id,))
    row = cur.fetchone()
    prev_ranks[page_id] = row[0] 



for key, value in outbound_links.items():
    print(f'({key} -> {value})')

print('\nINBOUND STARTS')
for key, value in inbound_links.items():
    print(f'({key} -> {value})')

print('\nPREV_RANKS DICTIONARY')

for key, value in prev_ranks.items():
    print(f'({key} -> {value})')


'''
page_rank(current_node) 
    = sum( ( prev_rank of the node_i pointing to current_node / no of outbound links from node_i ) )

take the above sum for all nodes pointing to current node
'''
next_ranks = {}

iteration_times = int(input("Enter the iteration amount: "))

if iteration_times < 1:
    print("\nMust iterate atleast once!\n")
    sys.exit()
    
for _ in range(iteration_times):
    for page_id, links_to in outbound_links.items():
        # only calculating page_rank for outbound liks 
        # as those are the only ones 100% guarenteed to have been retrieved
        next_rank = 0

        if page_id in inbound_links:
            for node_pointing_to_current_node in inbound_links[page_id]:
                next_rank += ( prev_ranks[node_pointing_to_current_node] / len(links_to) )
    
        next_ranks[page_id] = next_rank

    prev_ranks = next_ranks



print('\nNEXT_RANKS DICTIONARY')

for key, value in next_ranks.items():
    print(f'({key} -> {value})')


# update ranks in the database

for page_id, prev_rank in prev_ranks.items():
    cur.execute("UPDATE Pages SET old_rank = ? WHERE id = ?", (prev_rank, page_id))

for page_id, new_rank in next_ranks.items():
    cur.execute("UPDATE Pages SET new_rank = ? WHERE id = ?", (new_rank, page_id))


connection.commit()
cur.close()







