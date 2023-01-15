#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 17:21:00 2022

@author: Maarten Boneschansker
"""

import pandas as pd
import seaborn as sns
import re
import sys

# TODO start using regex for file names
# read data from each text file. 
file = str(sys.argv[1])
aacons=pd.read_csv(file, index_col=0, header=None, delimiter=' ').T
aacons.drop(index=aacons.index[-1], axis=0, inplace=True)
method = '#ZVELIBIL'
#normailze
aacons=(aacons-aacons.mean())/aacons.std()

if sum(aacons[method])==0:
	print('aacon score 0')
	quit()
	
#normailze
aacons=(aacons-aacons.mean())/aacons.std()

bins = 9
binsize = int(len(aacons)/ bins)
'''
because of rounding only once, you get either a little less or a little more bins
'''

aacons['Percentile'] = None

for i in range(len(aacons)+1):
    aacons['Percentile'][i]= round(i // binsize)+1
    #create list of exactly right size

#titel = re.search('*/*(.+?).fasta*', str(file)).group(1)
titel = file[6:]
print(titel)
    
sns.set_theme()
plot = sns.barplot(data=aacons, x='Percentile',  
                   y=(aacons[method]-aacons[method].mean())/aacons[method].mean(),
                   palette='Blues_d',
                   saturation=0.5, capsize=0.2, errwidth=1.5)

plot.set(xlabel = "precursor segment", 
         ylabel = 'Rel. Con. Score ' + str(round(aacons[method].mean(), 2)),
         title=titel)

plot2 = sns.relplot(data=aacons, x='Percentile', 
                    y=method, kind='line' )
plot2.set(xlabel = "precursor segment", ylabel = "Conservation Score", 
          title=titel, xticks=range(1,11))

plot3 = sns.relplot(data=aacons[method], kind='line' )
plot3.set(xlabel = "Residue", ylabel = "conservation score", title=titel)


plot2.refline(y = aacons[method].mean(), color='red', label=True)
plot3.refline(y = aacons[method].mean(), color='red', label=True)

plot.figure.savefig(file+method+'_barbinplot.png', dpi=300, bbox_inches='tight')
plot2.figure.savefig(file+method+'_linebinplot.png', dpi=300, bbox_inches='tight')
plot3.figure.savefig(file+method+'_lineplot.png', dpi=300, bbox_inches='tight')






