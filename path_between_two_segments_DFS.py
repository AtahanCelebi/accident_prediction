import csv
import sys

def convertPath2SQL(path):
    sql_string = ''
    for i in range(len(path)):
        tmp = ' "id" = ' + path[i] + " or " 
        sql_string = sql_string + tmp
    print(sql_string)

adj_matrix = dict()
visited = dict()

with open('segdict.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are:', row)
            line_count += 1
        elif(line_count==1): # strangely there is an empty line
            print(row)
            line_count += 1
        elif(line_count>=1):
            #print("Eleman sayisi: ", len(row), row)
            adj_matrix[row[0]] = row[1:len(row)-1]
            visited[row[0]] = False
            #print("Segment", row[0], "'s neighbors:",  adj_matrix[row[0]])
            line_count += 1

print(adj_matrix['1553049']) #OK

# Depth-First Search (DFS) implementation
# A better algorithm is Dijkstra, since DFS is more time consuming
   # We can assume equal cost for all segments
   # The only criterion is the road_class
   # Future work: investigate this functionaliy in QGIS
def printAllPaths(adj_matrix, u, d, visited, path):
    # Mark the current node as visited and store in path
    visited[u]= True
    path.append(u)

    # If current vertex is same as destination, then print current path[]
    if(u == d):
        print(path)
        found = 1
        sys.exit(0)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in adj_matrix[u]:
            if visited[i]== False:
                printAllPaths(adj_matrix, i, d, visited, path)
                      
    # Remove current vertex from path[] and mark it as unvisited 
    path.pop() 
    visited[u]= False




path = []


printAllPaths(adj_matrix, '5753448', '1596841', visited, path)

#If the path is copied and provided as an input to convertPath2SQL, it would return the SQL string
# In this way, the result could be checked in QGIS


