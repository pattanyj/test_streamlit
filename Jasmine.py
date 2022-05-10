#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:24:06 2022

@author: tales
"""


import pandas as pd
import numpy as np
import io
from zipfile import ZipFile
import os
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import networkx as nx
import matplotlib.cm as cm
import matplotlib
from matplotlib.cm import ScalarMappable
import matplotlib as mpl



#wgi
def get_wgi(year = 2018):
    wgi_files = pd.ExcelFile('wgidataset.xlsx').sheet_names
    
    wgi = []

    for file in wgi_files[1:]:
            wgi_d = pd.read_excel('wgidataset.xlsx', sheet_name= file, skiprows = 13, header = [0,1], index_col=[0,1])[[(year, 'Estimate')]]
            wgi_d.columns = [file]
            wgi.append(wgi_d)
    wgi = pd.concat(wgi, axis=1)
    wgi = wgi.mean(axis=1).reset_index()
    wgi.columns = ['Country/Territory', 'country', 'WGI']

    return wgi



year = 2018
alfa_thold = 0.4
hs_code = '841013'

wgi = get_wgi(year)


#BACI database
#data = pd.read_csv('Data/BACI_HS17_V202201//BACI_HS17_Y' + str(year) + '_V202201.csv', converters = {'k': str})
data = pd.read_csv('Data_test.csv')
data['q'] = pd.to_numeric(data['q'], errors='coerce')
data = data.dropna(subset=['q'])
data = data[data['k']==int(hs_code)]


#remove some minor countries from BACI without WGI correspondence and without WGI values (NA) --> 
countries_corr = pd.read_excel('correspondence_BACI_WGI.xlsx', sheet_name = 'Correspondence')
countries_corr = countries_corr[['Country/Territory', 'country', 'country_code']].dropna()

data = data[(data['i'].isin(list(countries_corr['country_code']))) & (data['j'].isin(list(countries_corr['country_code'])))]

#alfa, betweeness centrality and WGI
    


g = nx.from_pandas_edgelist(data, source = 'i', target = 'j', edge_attr = 'q', create_using=nx.DiGraph)
df_bet_cent = nx.betweenness_centrality(g) 
   
df_bet_cent = pd.DataFrame.from_dict(df_bet_cent, orient='index').reset_index()
df_bet_cent.columns = ['country_code', 'centrality_value']
    
    
norm = mpl.colors.Normalize(vmin=-2.5, vmax=2.5) 



#network 
def plot_network(hs_code):
    cent = df_bet_cent
    data_f = data[data['k']==int(hs_code)].copy()[['i', 'j', 'q']].dropna()
    unique_countries = list(pd.unique(data_f[['i', 'j']].values.ravel('K')))
    
    net_nodes = countries_corr[countries_corr['country_code'].isin(unique_countries)]
    net_nodes = pd.merge(net_nodes, wgi, how='left', on='country')
    net_nodes = pd.merge(net_nodes, cent, how='left', on='country_code')
    
    sizes = list(net_nodes['centrality_value']*100 + 0.001)

    nt = Network()
    nt.add_nodes(list(net_nodes['country_code']),
                 label = list(net_nodes['country']),
                 size = sizes,
                 color  = [matplotlib.colors.rgb2hex(cm.seismic_r(norm(x))) for x in net_nodes['WGI']])
    
    for index, row in data_f.iterrows():
        nt.add_edge(row['i'], row['j'], weight=row['q']/(data_f['q'].sum()))
    
    #plt.colorbar()
    nt.show('Jasmine.html')

    return

plot_network(hs_code = '841013')




















