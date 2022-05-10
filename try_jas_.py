# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:28:49 2022

@author: patta
"""

# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
# 2019-2020_LithiumIon.html

# Read dataset

df_interact = pd.read_csv('./network_product_data/libattery_nodes_2020_subtract_2019.csv')


# Set header title
st.title('Network Graph Visualization of Lithium Ion Trade Interactions')

# Define selection options and sort alphabetically
HS12_country = pd.read_csv('./BACI_HS12/country_codes_V202201.csv',encoding='unicode_escape')
country_list = list(HS12_country['country_name_full'])
country_list.sort()

# Implement multiselect dropdown menu for option selection
selected_country = st.multiselect('Select country or countries to visualize', country_list)


# Set info message on initial site load
if len(selected_country) == 0:
    st.text('Choose at least 1 country to get started')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['sources'].isin(selected_country) | \
                                df_interact['targets'].isin(selected_country)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'sources', 'targets', 'q')

    # Initiate PyVis network object
    drug_net = Network(height="800px", width="100%", directed=True, bgcolor='white', font_color='black')   #

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)
    
    # add edges    
    # edge_data = zip(sources, targets, weights)
        
    # for e in edge_data:
    #     src = e[0]
    #     dst = e[1]
    #     w = e[2]

    #     drug_net.add_node(src, src, title=src)
    #     drug_net.add_node(dst, dst, title=dst)
    #     drug_net.add_edge(src, dst, value=w)

    # # Generate network with specific layout settings
    drug_net.repulsion(node_distance=420, central_gravity=0.33,
                        spring_length=110, spring_strength=0.10,
                        damping=0.95)

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        # path = '/tmp'
        drug_net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        # path = '/html_files'
        drug_net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 1200,width=1000, scrolling = True)