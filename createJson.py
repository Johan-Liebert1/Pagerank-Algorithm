import sqlite3, sys

conn = sqlite3.connect('spider_database.sqlite')
cur = conn.cursor()

no = input("How many nodes to visualize in graph? > ")

if len(no) < 1:
    print("ATLEAST TWO NODES REQUIRED")
    sys.exit()

no_of_nodes = int(no)

cur.execute("""
    SELECT COUNT (from_page_id) AS inbound_links, old_rank, new_rank, id, url 
    FROM Pages JOIN Links ON Pages.id = Links.to_page_id
    WHERE html IS NOT NULL AND ERROR IS NULL
    GROUP BY id ORDER BY id, inbound_links
""")

file = open('graph.js','w')

nodes = []

maxrank = None
minrank = None

for row in cur:
    nodes.append(row)
    rank = row[2]
    
    if maxrank is None or maxrank < rank: 
        maxrank = rank

    if minrank is None or minrank > rank: 
        minrank = rank

    if len(nodes) > no_of_nodes: 
        break

if maxrank == minrank or maxrank is None or minrank is None:
# if maxrank is None or minrank is None:
    print("Error - please run pagerank.py to compute page rank")
    sys.exit()

file.write('spiderJson = {"nodes":[\n')
count = 0
map1 = {}
ranks = {}

for row in nodes:
    if count > 0: 
        file.write(',\n')

    rank = row[2]
    rank = 19 * ( (rank - minrank) / (maxrank - minrank) )

    file.write('{'+'"weight":'+str(row[0])+',"rank":'+str(rank)+',')
    file.write(' "id":'+str(row[3])+', "url":"'+row[4]+'"}')

    map1[row[3]] = count
    ranks[row[3]] = rank
    count = count + 1
file.write('],\n')

cur.execute('''SELECT from_page_id, to_page_id FROM Links''')
file.write('"links":[\n')

count = 0
for row in cur :
    if row[0] not in map1 or row[1] not in map1 : 
        continue

    if count > 0 : 
        file.write(',\n')

    rank = ranks[row[0]]
    srank = 19 * ( (rank - minrank) / (maxrank - minrank) ) 
    file.write('{"source":'+str(map1[row[0]])+',"target":'+str(map1[row[1]])+',"value":3}')
    count += 1
    
file.write(']};')
file.close()
cur.close()

print("Open view.html in a browser to view the visualization")
