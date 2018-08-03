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
with open('data/oathbringer.txt') as text:
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
characters = [' Syl ', ' Pattern ', 'Wyndle ', 'Glys ', ' Ivory ', ' Timbre ', 'Stormfather ',
              'Nightwatcher ', 'Dalinar ', 'Shallan ', 'Kaladin ', 'Venli ', 'Adolin ', 
              'Szeth ', 'Navani ', 'Moash ', 'Jasnah ', 'Teft ', 'Renarin ', 'Lift ', 
              'Taravangian ', 'Wit ', 'Eshonai ', ' Rock ', 'Lopen ', 'Rysn ', 'Sigzil ',
              'palona ', 'mem ', 'ellista ', 'kaza ', 'gawx ', 'sheler ', 'rlain ',
              'torol ', 'meridas ', 'teleb ', 'gavilar ', 'resi ', 'elit ', 'erraniv ',
              'helaran ', 'jakamav ', 'kalishor ', 'salinor ', 'tanalor ', 'tinalar ',
              'skar ', 'dabbid ', 'hobber ', 'shen ', 'leyten ', 
              'drehy ', 'gadol ', 'natam ', 'peet ', 'torfin ', 'yake ', 'baxil ', 
              'roshone ', 'tavinar ', 'istow ', 'dukar ', 'gavinor ', 'gaz ', 'ghenna ', 
              'hoid ', 'inadara', 'isasik', 'ishikk', 'jenet', 'kadash', 'kalami', 
              'khal ', 'khriss', 'laral ', 'lhan ', 'lirin', 'maben', 
              'maib ', 'marri ', 'mik ', 'nale ', 'nazh', 'nergaoul', 'nbissiquan', 
              'nlent', 'noura', ' odium', 'redin', 'rez ', 'rial', 'rushu',
              'sebarial', 'shalash', 'sidin', 'sja-anat', 'tag ', 'taka ',
              'talik', 'temoo', 'thresh ', 'tigzikk', 'toravi', 'vamah', 
              'vao', 'vath ', 'vathah', ' veil ', 'elhokar', ' evi ', 
              'evinor']
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
edge_list = [] #test networkx
for index, row in df.iterrows():
    i = 0
    for col in row:
        weight = float(col)/464
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
        
#networkx graph time!
G = nx.Graph()
for i in sorted(node_list):
    G.add_node(i[0], size = i[1])
G.add_weighted_edges_from(updated_edge_list)

#check data of graphs
G.nodes(data=True)
G.edges(data = True)

node_order = ['Skar ', ' Syl ', 'Rushu', 'Kaza ', 'Peet ', 'Roshone ', 'Dabbid ',
              'Toravi', 'Natam ', 'Adolin ', 'Shallan ', 'Navani ', 'Nightwatcher ', 
              'Gavilar ', 'Rlain ', ' Odium', 'Khal ', 'Ellista ', 'Lirin', 'Leyten ',
              'Laral ', 'Torol ', 'Shalash', 'Inadara', 'Sigzil ', 'Elhokar', 'Venli ', 
              'Sidin', 'Wyndle ', 'Rysn ', 'Mem ', 'Palona ', 'Wit ', 'Vamah', 'Eshonai ', 
              'Lift ', 'Stormfather ', ' Evi ', 'Moash ', 'Shen ', 'Kaladin ', 'Lopen ', 
              'Szeth ', 'Renarin ', 'Taravangian ', 'Kadash', 'Nale ', 'Drehy ', 'Dukar ', 
              'Gaz ', 'Teleb ', 'Helaran ', 'Sheler ', 'Sebarial', 'Hoid ', 'Meridas ', 
              ' Pattern ', ' Timbre ', 'Kalami', 'Glys ', 'Yake ', ' Veil ', 'Nergaoul', 
              'Noura', 'Hobber ', ' Ivory ', 'Maben', 'Torfin ', 'Rial', 'Teft ', 'Dalinar ', 
              'Vathah', 'Jakamav ', 'Jasnah ', ' Rock ']

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
    for x in test.iterkeys():
        if i[0] == x[0] and i[1] == x[1]:
            updated_again_edges.append(test[x])
            
#drawing custimization
sizes = [x[1]*200 for x in updated_node_order]
widths = [x*4.5 for x in updated_again_edges]

#draw the graph
pos = nx.spring_layout(G, k=0.42, iterations=18)

nx.draw(G, pos, with_labels=True, font_size = 6.5, font_weight = 'bold', 
        node_size = sizes, width = widths)

plt.axis('off')
plt.savefig("weighted_graph.png") # save as png