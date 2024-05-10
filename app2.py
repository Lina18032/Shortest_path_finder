import osmnx as ox
import pandas as pd
import networkx as nx
import streamlit as st
import folium
from streamlit_folium import folium_static

#loading the map of jijel , Algeria
city = "Jijel, Algeria"
graph = ox.graph_from_place(city, network_type="all")
#loading dataframe
node_data = pd.read_csv("node_data.csv")

#find the nearest node based on latitude and longitude
def nearest_node(graph, lat, lon):
    node = ox.distance.nearest_nodes(graph, lon, lat)
    return node

# Streamlit UI
st.title("Shortest Path Finder")

# Create a Folium map centered on Jijel, Algeria
m = folium.Map(location=[36.8167, 5.7667], zoom_start=12)

# Add graph edges to Folium map
for u, v, data in graph.edges(data=True):
    folium.PolyLine(locations=[(graph.nodes[u]['y'], graph.nodes[u]['x']),
                                (graph.nodes[v]['y'], graph.nodes[v]['x'])],
                    color='white', weight=2).add_to(m)

# Choose source and target nodes
source_name = st.selectbox("Where you are ?", node_data['name'].tolist())
target_name = st.selectbox("Where do you want to go ?", node_data['name'].tolist())

# Find the nearest node to the selected source and target node names
source_data = node_data[node_data['name'] == source_name]
target_data = node_data[node_data['name'] == target_name]

if not source_data.empty and not target_data.empty:
    source = nearest_node(graph, source_data['lat'].iloc[0], source_data['lon'].iloc[0])
    target = nearest_node(graph, target_data['lat'].iloc[0], target_data['lon'].iloc[0])
else:
    st.error("One or more node names not found!")

if st.button("Choose the best Path"):
    # Find the shortest path using A* algorithm
    shortest_path_nodes = nx.astar_path(graph, source, target, weight='length')

    # Add shortest path to Folium map
    shortest_path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path_nodes]
    folium.PolyLine(locations=shortest_path_coords, color='red', weight=6).add_to(m)

    # Display the map
    folium_static(m)
