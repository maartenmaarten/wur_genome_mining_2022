#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:35:00 2022

@author: Maarten Boneschansker

Goal: to get from lots of aacon files to one big csv, which can be used for
SOM analysis. 
Needs segments + ripp or not as columns
Needs precursor/peptide name as row
as such



"""

import pandas as pd
import re
import sys
import glob
import os


# TODO start using regex for file names
# read data from each text file. 
folder = str(sys.argv[1])
ripp = str(sys.argv[2]) # either 1 or 0
project_name = str(sys.argv[3])

print(folder)
methods = ['#KABAT', '#JORES', '#SCHNEIDER', '#SHENKIN', '#GERSTEIN',
'#TAYLOR_GAPS', '#TAYLOR_NO_GAPS', '#ZVELIBIL', '#KARLIN', '#ARMON',
'#THOMPSON', '#NOT_LANCET', '#MIRNY', '#WILLIAMSON', '#LANDGRAF',
'#SANDER', '#VALDAR', '#SMERFS']

print(ripp)

file_list = glob.glob(folder+'*aacon')


def average_dataframe(input_dataframe, bins):
    # outputs dataframe with averages of #bins
    dataframe_average = pd.DataFrame()
    binsize = len(input_dataframe)/bins # outputs float number
    
    # TODO dit moet je checken, not entirely right!
    for i in range(bins):
        dataframe_average[i] = round(input_dataframe.iloc[round(i*binsize):\
                                                    round((i+1)*binsize)].mean(),2)

    # mean() transposes out horizontally so needs .T
    return dataframe_average.T
    
    

def aacons_to_som(input_dataframe, method, name):
    aacons_to_som = pd.DataFrame()
    aacons_to_som[0] = input_dataframe[method]
    aacons_to_som = aacons_to_som.T
    aacons_to_som['PRECURSOR'] = name
    aacons_to_som['METHOD'] = method
    aacons_to_som['RIPP'] = ripp
    # but this is just one line
    return aacons_to_som.T

for method in methods:
    csv = pd.DataFrame()
    for i,j in enumerate(file_list):
        path, name = os.path.split(j)
        aacons=pd.read_csv(j, index_col=0, header=None, delimiter=' ').T
        aacons.drop(index=aacons.index[-1], axis=0, inplace=True)
        normalized_aacons=(aacons-aacons.mean())/aacons.std()

        csv[i] = aacons_to_som(average_dataframe(aacons, 10), 
                               method, name[:30])
        print(csv[i])
    
    csv.T.to_csv(folder+project_name+method+'normalized_aacon_decrippter.csv')

