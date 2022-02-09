#!/usr/bin/env python

# There are 606 parent proteins. This script creates a unique color for each parent protein. 
import re

protein_file = open("Parent_Protein_Names.txt", "r")
protein_list = []
for line in protein_file:
  protein_list.append(line.rstrip('\n'))
#print(protein_list)
import random 
 
def colors(n): 
  ret = [] 
  r = int(random.random() * 607) 
  g = int(random.random() * 607) 
  b = int(random.random() * 607) 
  step = 607 / n 
  for i in range(n): 
    r += step 
    g += step 
    b += step 
    r = (int(r) % 607) 
    g = (int(g) % 607) 
    b = (int(b) % 607) 
    r_string = str(r).rstrip("'")
    g_string = str(g).rstrip("'")
    b_string = str(b).rstrip("'")
    rgb_string = 'rgb(' + r_string + "," + g_string + "," + b_string + ')'

    # 'rgb(245,138,94)'

    ret.append(rgb_string)  
  return ret

colors_list = colors(606)

color_palette = {}
color_count = 0
for i in protein_list:
    color_palette[i] = colors_list[color_count]
    color_count += 1
print(color_palette)

