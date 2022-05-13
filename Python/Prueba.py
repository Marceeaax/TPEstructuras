import requests
import time
import csv
from datetime import datetime
import datetime
from bs4 import BeautifulSoup
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


lenguajes = ['Python', 'C', 'Java', 'C++', 'C#', 'Visual Basic', 'JavaScript', 'Assembly language', 'SQL', 'PHP', 'R', 'Delphi/Object Pascal', 'Go', 'Swift', 'Ruby', 'Classic Visual Basic', 'Objective-C', 'Perl', 'Lua', 'MATLAB']
repositorios = [275079, 43737, 163690, 45193, 46701, 912, 305721, 4722, 24021, 89460, 26173, 1890, 41607, 33834, 28159, 66, 5460, 3832, 9568, 9633]
rating = [89.97497178191097, 14.287677283211464, 53.532250413047386, 14.764031342526703, 15.25739804681749, 0.27678264710212497, 100.0, 1.5232860578102763, 7.8372675074839275, 29.246699710457868, 8.541329276471838, 0.5967512391421701, 13.590813171713206, 11.04774991411886, 9.19108144803782, 0.0, 1.7647347499631938, 1.2321080957288446, 3.1087337030311954, 3.129999509250626]

titulos = ['NOMBRE_LENGUAJE','NUMERO_APARICIONES']

listaTopics = {'TOPIC': ['java', 'spring-boot', 'spring', 'python', 'javascript', 'android', 'mysql', 'kotlin', 'leetcode', 'sql', 'maven', 'cpp', 'minecraft', 'hacktoberfest', 'algorithms', 'database', 'docker', 'data-structures', 'springboot', 'algorithm'], 'NRO_APARICIONES': [944, 92, 73, 71, 66, 53, 52, 45, 43, 41, 38, 36, 36, 34, 31, 26, 26, 24, 24, 23]}

df=pd.DataFrame(listaTopics)

fig,ax = plt.subplots(figsize=(20,6))

fig.patch.set_facecolor('black')

sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)

csfont = {'fontname':'Source Code Pro'}

sns.barplot(x='TOPIC',y='NRO_APARICIONES',data=df,ci=95,palette="crest",ax=ax,color='white')

ax.set_title("TEMA 2\nTopics asociados de los repositorios actualizados en los últimos 30 días",**csfont,color='white')

ax.tick_params(axis='y',labelsize=16,length=0,colors='gray')
ax.tick_params(axis='x',labelsize=8,length=0,pad=2,colors='grey')

# method 1
ax.spines['left'].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
#method 2
plt.box(False)

# add grid lines for y axis
ax.yaxis.grid(linewidth=0.5,color='gray')
# put the grid lines below bars
ax.set_axisbelow(True)

ax.set_xlabel('TOPIC',labelpad=-5,weight='bold',size=10,**csfont,c='grey')
ax.set_ylabel('NRO_APARICIONES',labelpad=15,weight='bold',size=15,**csfont,c='grey')

plt.xticks(rotation=30,color='#565656')

plt.show()

