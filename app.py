#####################
# Code Overview
#   Run this code by entering the following into the terminal:
#   streamlit run "path_to_code"
# This should prompt you a url to view the map.
# More instructions on how to install libraries are in the github README.md
######################


import googlemaps
import pandas as pd
import folium 
from folium.plugins import FeatureGroupSubGroup
import streamlit as st
from streamlit_folium import st_folium
import yaml


with open('config.yaml', "r") as file:
    config = yaml.safe_load(file)
    api_key = config.get("api_key")

gmaps = googlemaps.Client(key=api_key)
ingham_county = gmaps.geocode('Ingham County, MI')

lat, long = ingham_county[0]['geometry']['location']['lat'], ingham_county[0]['geometry']['location']['lng']
min_lon, max_lon = -84.1406009, -84.6031371
min_lat, max_lat = 42.4219371, 42.776639

m = folium.Map(
    max_bounds=True,
    location=[lat, long],
    zoom_start=11,
    min_lat=min_lat,
    max_lat=max_lat,
    min_lon=min_lon,
    max_lon=max_lon,
    scrollWheelZoom = False
)

folium.Rectangle(
    bounds=[[min_lat, min_lon], [max_lat, max_lon]],
    line_join="round",
    dash_array="5, 5"
).add_to(m)

# Function to fetch places
def get_places_query(query, county="Ingham County, Michigan"):
    places_result = gmaps.places(query=f"{query} in {county}")
    locations = []
    
    while True:
        for place in places_result.get("results", []):
            name = place["name"]
            lat = place["geometry"]["location"]["lat"]
            lng = place["geometry"]["location"]["lng"]
            locations.append({"name": name, "lat": lat, "lng": lng})
        
        # Handle pagination
        if "next_page_token" in places_result:
            import time
            time.sleep(2)  # Wait before requesting next page
            places_result = gmaps.places(query=f"{query} in {county}", page_token=places_result["next_page_token"])
        else:
            break
    
    return locations

def get_places_pandas(lat_series, lng_series, name_series):
    locations = []
    for i in range(len(lat_series)):
        locations.append({"name": name_series.iloc[i], "lat": lat_series.iloc[i], "lng": lng_series.iloc[i]})

    return locations

# Fetch locations
libraries = get_places_query("libraries")
parks = get_places_query("parks")
rec_centers = get_places_query("recreation centers")
soup_kitchens = get_places_query("soup kitchens")
bus_stops_csv = pd.read_csv("bus_stops.csv")
bus_stops = get_places_pandas(bus_stops_csv['stop_lat'], bus_stops_csv['stop_lon'], bus_stops_csv['stop_name'])

# Define feature groups for different layers
layer_community = folium.FeatureGroup(name="Community Connections", show=True)
layer_parks_rec = folium.FeatureGroup(name="Parks & Recreation", show=True)
layer_food_assistance = folium.FeatureGroup(name="Food Assistance", show=True)
layer_transportation = folium.FeatureGroup(name="Transportation", show=True)

# Subgroups for more organization
libraries_layer = FeatureGroupSubGroup(layer_community, "Libraries")
parks_layer = FeatureGroupSubGroup(layer_parks_rec, "Parks")
rec_centers_layer = FeatureGroupSubGroup(layer_parks_rec, "Recreation Centers")
soup_layer = FeatureGroupSubGroup(layer_food_assistance, "Soup Kitchens")
bus_stops_layer = FeatureGroupSubGroup(layer_transportation, "Bus Stops")

# Add places to layers
for place in libraries:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="blue", icon="book")
    ).add_to(libraries_layer)

for place in parks:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="green", icon="tree", prefix="fa")
    ).add_to(parks_layer)

for place in rec_centers:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="purple", icon="bicycle", prefix="fa")
    ).add_to(rec_centers_layer)

for place in soup_kitchens:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="beige", icon="bowl-food", prefix="fa")
    ).add_to(soup_layer)

for place in bus_stops:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="lightblue", icon="bus", prefix="fa")
    ).add_to(bus_stops_layer)

# Add layers to map
m.add_child(layer_community)
layer_community.add_child(libraries_layer)

m.add_child(layer_parks_rec)
layer_parks_rec.add_child(parks_layer)
layer_parks_rec.add_child(rec_centers_layer)

m.add_child(layer_food_assistance)
layer_food_assistance.add_child(soup_layer)

m.add_child(layer_transportation)
layer_transportation.add_child(bus_stops_layer)

# Add layer control to toggle visibility
folium.LayerControl(collapsed=False).add_to(m)

st.title("MSU Healthy City Assessment Map")
st_folium(m, width=700)