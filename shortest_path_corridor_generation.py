# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 16:57:59 2020
@author: banbar
"""
import csv
import networkx as nx

adj_matrix = dict()
visited = dict()

# Open the adjacency matrix provided
with open('segdictAllStatic.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are:', row)
            line_count += 1
        elif (line_count == 1):  # strangely there is an empty line
            print(row)
            line_count += 1
        elif (line_count >= 1):
            # print("Eleman sayisi: ", len(row), row)
            adj_matrix[row[0]] = row[1:len(row) - 1]
            visited[row[0]] = False
            # print("Segment", row[0], "'s neighbors:",  adj_matrix[row[0]])
            line_count += 1

# Create a directed graph
G = nx.DiGraph()

# Add the segments to the graph
# The cost of each segment is assumed to be 1 - this could be updated for different purposes
for segment in adj_matrix:
    for neigh in range(len(adj_matrix[segment])):
        G.add_weighted_edges_from([(segment, adj_matrix[segment][neigh], {'distance': 1})])

    # Tested for:
# Corridor: start segment (source) - end segment (target)
# 33.8.s_n: 2166736 - 646288
# 33.3.w_e: 1576735 - 6219404
# 33.12.s_n: 891088 - 4120267
# 33.13.w_e: 380239 - 2203929

# path = nx.shortest_path(G, source='891088', target = '4120267')

# Once the whole adjacency matrix is provided, another shorter path than the corridor might exist.
# For example, for the 33.13.w_e we have 279 segments, but the code generates a path with 263 segments.
# We need to update the code to accommadate multiple intermediate segments on the corridor path.

# Record a segment for every ~50 segments - better to test on longer corridors
cor_33_8_s_n = ['2166736', '1562368', '382917', '647449', '646288']
cor_33_3_w_e = ['1576735', '5702701', '6219404']
cor_33_12_s_n = ['891088', '888995', '4120267']
cor_33_13_w_e = ['380239', '655988', '657074', '648173', '646594', '647780', '2203929']
cor_33_6 = ["648457","975850","790663","2157356","4124266"]

# cor_33_1_e_w shows that we might need to select more frequently in urban areas
# It finds a shorter route at the very beginning, but the remaining is OK
cor_33_1_e_w = ['791686', '975840', '389266', '779975', '1576123', '646945', '646353', '1554776', '652345']


corridor_segments = cor_33_1_e_w

path = []
for c in range(len(corridor_segments) - 1):
    temp_path = nx.shortest_path(G, source=corridor_segments[c], target=corridor_segments[c + 1])
    # Remove the last element in the path - it will be included in the next iteration
    temp_path.pop()
    # if we path.append(temp_path), we will generate a 2D list. Instead copy each segment one-by-one
    for i in range(len(temp_path)):
        path.append(temp_path[i])

# Add the last segment of the corridor
path.append(corridor_segments[c + 1])

print(path)
print(len(path))
# To visualise the path in QGIS:
def convertPath2SQL(path):
    sql_string = ''
    for i in range(len(path)):
        tmp = ' "id" = ' + path[i] + " or "
        sql_string = sql_string + tmp
    print(sql_string)
    # convertPath2SQL(path)