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
characters = ['Syl ', 'Pattern ', 'Wyndle ', 'Glys ', 'Ivory ', 'Timbre ', 'Stormfather ',
              'Nightwatcher ', 'Dalinar ', 'Shallan ', 'Kaladin ', 'Venli ', 'Adolin ', 
              'Szeth ', 'Navani ', 'Moash ', 'Jasnah ', 'Teft ', 'Renarin ', 'Lift ', 
              'Taravangian ', 'Wit ', 'Eshonai ', 'Rock ', 'Lopen ', 'Rysn ', 'Sigzil ',
              'palona ', 'mem ', 'ellista ', 'kaza ', 'gawx ', 'sheler ', 'rlain ',
              'torol ', 'meridas ', 'teleb ', 'gavilar ', 'resi ', 'elit ', 'erraniv ',
              'helaran ', 'jakamav ', 'kalishor ', 'salinor ', 'tanalor ', 'tinalar ',
              'skar ', 'bisig ', 'dabbid ', 'hobber ', 'shen ', 'leyten ', 
              'drehy ', 'gadol ', 'natam ', 'peet ', 'torfin ', 'yake ', 'baxil ', 
              'roshone ', 'tavinar ', 'istow ', 'dukar ', 'gavinor ', 'gaz ', 'ghenna ', 
              'hoid ', 'inadara', 'isasik', 'ishikk', 'jenet', 'kadash', 'kalami', 
              'khal ', 'khriss', 'laral ', 'lhan ', 'lirin', 'maben', 
              'maib ', 'marri ', 'mik ', 'nale ', 'nazh', 'nergaoul', 'nbissiquan', 
              'nlent', 'noura', 'odium', 'redin', 'rez ', 'rial', 'rushu',
              'sebarial', 'shalash', 'sidin', 'sja-anat', 'tag ', 'taka ',
              'talik', 'temoo', 'thresh ', 'tigzikk', 'toravi', 'vamah', 
              'vao', 'vath ', 'vathah', 'veil ', 'elhokar', 'evi ', 
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
        
#networkx graph time!
G = nx.Graph()
G.add_nodes_from(characters)
G.add_weighted_edges_from(edge_list)

#customize graphs


#draw the graph
nx.draw(G)

#Edit here