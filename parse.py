# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:33:20 2018

@author: andyj
"""
import re
import pandas as pd


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
    cleaned_sections.append(section.lower())


#Create characters list and cooccurnce matrix
characters = ['syl', 'pattern', 'wyndle', 'glys', 'ivory', 'timbre', 'stormfather',
              'nightwatcher', 'dalinar', 'shallan', 'kaladin', 'venli', 'adolin', 
              'szeth', 'navani', 'moash', 'jasnah', 'teft', 'renarin', 'lift', 
              'taravangian', 'wit', 'eshonai', 'rock', 'lopen', 'rysn', 'sigzil',
              'palona', 'mem', 'ellista', 'kaza', 'gawx', 'sheler', 'rlain',
              'torol', 'meridas', 'teleb', 'gavilar', 'resi', 'elit', 'erraniv',
              'helaran', 'jakamav', 'kalishor', 'salinor', 'tanalor', 'tinalar',
              'teft', 'skar', 'bisig', 'dabbid', 'hobber', 'shen', 'leyten', 
              'drehy', 'gadol', 'natam', 'peet', 'torfin', 'yake', 'baxil', 
              'roshone', 'tavinar', 'istow', 'dukar', 'gavinor', 'gaz', 'ghenna', 
              'hoid', 'inadara', 'isasik', 'ishikk', 'jenet', 'kadash', 'kalami', 
              'khal', 'khriss', 'laral', 'lhan', 'lift', 'lirin', 'maben', 
              'maib', 'marri', 'mik', 'nale', 'nazh', 'nergaoul', 'nbissiquan', 
              'nlent', 'noura', 'odium', 'redin', 'rez', 'rial', 'rushu',
              'sebarial', 'shalash', 'sidin', 'sja-anat', 'tag', 'taka',
              'talik', 'temoo', 'thresh', 'tigzikk', 'toravi', 'vamah', 
              'vao', 'vath ', 'vathah', 'veil', 'venli', 'elhokar', 'evi ', 
              'evinor']

#--> iterate through each
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
            
    #count name of characters (only once per)
sections_df = pd.DataFrame(sections_dictionary.items()) 

    #update matrix