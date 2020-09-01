import sqlite3, sys

conn = sqlite3.connect('spider_database.sqlite')
cur = conn.cursor()

no = input("Enter the number of nodes to visualize in the graph > ")

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


graphNodes = []
maxRank = None
minRank = None

for row in cur:
    graphNodes.append(row)
    rank = row[2]

    if maxRank is None or maxRank < rank:
        maxRank = rank

    if minRank is None or minRank > rank:
        minRank = rank

    if len(graphNodes) == no_of_nodes:
        break

if maxRank == minRank or maxRank is None or minRank is None:
    print("ERROR! Please run pagerank.py to calculate page ranks")

# row = (noOfInboundLinks, old_rank, new_rank, id, url)

file = open("./scripts/graph.js", "w")
count = 0
mapping = {} # to map source node to target node
ranks = {}

file.write('const spiderJson = { \n "nodes" : [\n ')

for row in graphNodes:
    if count > 0:
        file.write(",\n")
    
    rank = row[2]

    # normalize ranks
    rank = 19 * ( (rank - minRank) / (maxRank - minRank) + 0.01 )

    data = '"weight" : {}, "rank" : {}, "id": {}, "url" : "{}"' \
            .format(str(row[0]), str(rank), str(row[3]), row[4])

    file.write('{' + data + '}' )

    mapping[row[3]] = count
    ranks[row[3]] = rank

    count += 1

cur.execute('''SELECT from_page_id, to_page_id FROM Links''')
file.write('],\n"links" : [\n')

count = 0

for row in cur :
    if row[0] not in mapping or row[1] not in mapping : 
        continue

    if count > 0 : 
        file.write(',\n')

    rank = ranks[row[0]]

    data = '"source" : {}, "target" : {}' \
            .format(str(mapping[row[0]]), str(mapping[row[1]]))

    file.write('{' + data + '}')

    count += 1
    
file.write('\n]\n}')

file.close()
cur.close()

print("Successfully wrote data to graph.js")
print("Open view.html to view the pagerank graph")