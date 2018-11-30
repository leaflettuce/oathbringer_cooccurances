# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:33:20 2018

@author: andyj
"""
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#import
with open('data/brothers.txt', encoding = 'utf8') as text:
    book_text = text.read()

#split at pov changes
book_text = book_text.replace('—From', ' * * * ')
sections = book_text.split('* * *')

#remove all dialogue
cleaned_sections = []

for section in sections:
    quotes = re.findall("“.*?”", section)
    for quote in quotes:
        section = section.replace(quote, " ")
    cleaned_sections.append(section)


#Create characters list and cooccurnce matrix
characters = ['Alyosha', 'Dmitri', 'Ivan', 'Fyodor', 'Agrafena', 'Pavel', 
              'Zosima', 'Katerina', 'Khokhlakov', 'Lisa', 'Mikhail', 
              'Pyotr', 'Kuzma', 'Lizaveta', 'Fetyukovich', 'Ippolit', 
              'Ferapont', 'Nikolai', 'Ilyusha', 'Grigory']
characters = [character.title() for character in characters] #oops title case

#--> iterate through each and store in dictionary
sections_dictionary = {}
iterative = 0
for section in cleaned_sections:
    iterative += 1
    for char in characters:
        if char in section:
            if str(iterative) in sections_dictionary.keys():
                sections_dictionary[str(iterative)].append(char)  
            else:
                sections_dictionary[str(iterative)] = [char]                      
            
##set base df (co-occurance matrix)
df = pd.DataFrame(columns = characters, index = characters)
df[:] = int(0)

#iterate through each POV of book and add one for each character-character relationship
#-> in this case, relationship equates to appearing in the same POV
for value in sections_dictionary.values():
    for character1 in characters:
        for character2 in characters:
            if character1 in value and character2 in value:
                df[character1][character2] += 1
                df[character2][character1] += 1
                
#add weights to edges
weight_denominator = 32
edge_list = [] #test networkx
for index, row in df.iterrows():
    i = 0
    for col in row:
        weight = float(col)/weight_denominator
        edge_list.append((index, df.columns[i], weight))
        i += 1

#Remove edge if 0.0
updated_edge_list = [x for x in edge_list if not x[2] == 0.0]

#create duple of char, occurance in novel
node_list = []
for i in characters:
    for e in updated_edge_list:
        if i == e[0] and i == e[1]:
           node_list.append((i, e[2]*6))
for i in node_list:
    if i[1] == 0.0:
        node_list.remove(i)

#remove self references
for i in updated_edge_list:
    if i[0] == i[1]:
        updated_edge_list.remove(i)
        
        
        
# Print out duple as csv
import csv
version  = 'data/brothers_'
n_header = ['person', 'weight']
n_filename = 'node_weights'                #Change to desired csv filename

with open(version + n_filename + '.csv', 'w') as f: # replace 'w' with 'wb' for python 2
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(n_header)
    for i in node_list:
        writer.writerow([i[0], i[1]])

# Print out tuple as csv
e_header = ['person1', 'person2', 'weight']
e_filename = 'edge_list'                #Change to desired csv filename

with open(version + e_filename + '.csv', 'w') as f: # replace 'w' with 'wb' for python 2
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(e_header)
    for i in updated_edge_list:
        writer.writerow([i[0], i[1], i[2]])


#### print out matrix
m_filename = 'matrix'
df.to_csv(version + m_filename + '.csv')



#set canvas size
plt.subplots(figsize=(14,14))

#networkx graph time!
G = nx.Graph()
for i in sorted(node_list):
    G.add_node(i[0], size = i[1])
G.add_weighted_edges_from(updated_edge_list)

#check data of graphs
#G.nodes(data=True)
#G.edges(data = True)

#manually copy and pasted the node order using 'nx.nodes(G)'
#Couldn't determine another route to listing out the order of nodes for future work
node_order = ['Fyodor', 'Agrafena', 'Ferapont', 'Lizaveta', 'Katerina', 'Alyosha', 'Ivan', 
              'Grigory', 'Pyotr', 'Dmitri', 'Kuzma', 'Pavel', 'Ippolit']

#reorder node list
updated_node_order = []
for i in node_order:
    for x in node_list:
        if x[0] == i:
            updated_node_order.append(x)
            
#reorder edge list - this was a pain
test = nx.get_edge_attributes(G, 'weight')
updated_again_edges = []
for i in nx.edges(G):
    for x in test.keys():
        if i[0] == x[0] and i[1] == x[1]:
            updated_again_edges.append(test[x])
            
#drawing custimization
node_scalar = 800
edge_scalar = 8
sizes = [x[1]*node_scalar for x in updated_node_order]
widths = [x*edge_scalar for x in updated_again_edges]

#draw the graph
pos = nx.spring_layout(G, k=0.42, iterations=17)

nx.draw(G, pos, with_labels=True, font_size = 8, font_weight = 'bold', 
        node_size = sizes, width = widths)

plt.axis('off')
plt.savefig("imgs/brothers.png") # save as png