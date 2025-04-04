#import googlemaps
import pandas as pd
import folium 
from folium.plugins import FeatureGroupSubGroup
import streamlit as st
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
import hashlib

#OUTDATED GOOGLE MAPS CODE
#gmaps = googlemaps.Client(key)
#ingham_county = gmaps.geocode('Ingham County, MI')
#lat, long = ingham_county[0]['geometry']['location']['lat'], ingham_county[0]['geometry']['location']['lng']

min_lon, max_lon = -84.1406009, -84.6031371
min_lat, max_lat = 42.4219371, 42.776639

#Census Tract Info
green_zones = ["26065003301", "26065006600", "26065006700", "26065003700", "26065003602",
"26065005100", "26065005303", "26065005402", "26065004301"]
gdf = gpd.read_file("PVS_24_v2_tracts2020_26.shp")
gdf = gdf[gdf['TRACTID'].isin(green_zones)]

#Green Zones Demographic Info
elderly = pd.read_csv('elderly_data_complete.csv')
elderly = elderly[elderly['GEO_ID'].isin(green_zones)]
elderly['GEO_ID'] = elderly['GEO_ID'].astype(str)
elderly = elderly.rename(columns={"GEO_ID": "TRACTID"})

#Merging Census Tract & Green Zones
gdf = gdf.merge(elderly, "left", "TRACTID")

#Making Health Index
features = ["percent below poverty line", "number covered by medicare", 
"number covered by medicaid", "number living alone"]

def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

df_normalized = gdf.copy()
for feature in features:
    df_normalized[feature] = min_max_scale(gdf[feature].astype(float))

weights = {
    "percent below poverty line": 0.5,  # High weight for poverty impact
    "number covered by medicare": -0.25,  # Negative impact (more coverage = better health)
    "number covered by medicaid": -0.25,  # Negative impact
    "number living alone": 0.3,  # High weight for social isolation impact
}

df_normalized["health_score"] = sum(df_normalized[feature] * weight for feature, weight in weights.items())

gdf = gdf.merge(df_normalized.loc[:,["TRACTID", "health_score"]], "left", "TRACTID")


#Hash map coloring
# Get min and max health score for normalization
min_score = df_normalized["health_score"].min()
max_score = df_normalized["health_score"].max()

def get_tract_color(health_score, min_score, max_score):
    norm_score = (health_score - min_score) / (max_score - min_score)  # Normalize between 0 and 1
    r = int(255 * norm_score)
    g = int(255 * (1 - norm_score))
    b = 0
    return f'#{r:02x}{g:02x}{b:02x}'  # Convert to hex color

def get_tract_color_from_df(tract_id, df_final, min_score, max_score):
    # Find the row corresponding to the tract_id in df_final and get the health_score
    health_score = df_final[df_final['TRACTID'] == tract_id]['health_score'].values[0]
    return get_tract_color(health_score, min_score, max_score)

#Making Map
m = folium.Map(
    max_bounds=True,
    location=[42.599288, -84.371869],
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

#Adding Census Tracts
folium.GeoJson(
    gdf,
    name="Green Zones",
    tooltip=folium.GeoJsonTooltip(fields=["NAME", "population of old people", "percent below poverty line", "number covered by medicare", "number covered by medicaid", "number living alone"], 
                                  aliases=["CENSUS #:", "65+ Population:", "65+ % Below Poverty Line:", "65+ On Medicare:", "65+ On Medicaid:", "65+ Living Alone:"]),
    popup=folium.GeoJsonPopup(fields=["TRACTID", "POP20", "health_score"]),
    style_function=lambda feature: {
        "fillColor": get_tract_color(feature["properties"]["health_score"], min_score, max_score),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    }
).add_to(m)

# Function to fetch places

#def get_places_query(query, county="Ingham County, Michigan"):
#    places_result = gmaps.places(query=f"{query} in {county}")
 #   locations = []
    
  #  while True:
   #     for place in places_result.get("results", []):
    #        name = place["name"]
     #       lat = place["geometry"]["location"]["lat"]
     #       lng = place["geometry"]["location"]["lng"]
      #      locations.append({"name": name, "lat": lat, "lng": lng})
        
        # Handle pagination
      #  if "next_page_token" in places_result:
      #      import time
      #      time.sleep(2)  # Wait before requesting next page
      #      places_result = gmaps.places(query=f"{query} in {county}", page_token=places_result["next_page_token"])
      #  else:
      #      break
    
    #return locations

def get_places_pandas(lat_series, lng_series, name_series):
    locations = []
    for i in range(len(lat_series)):
        locations.append({"name": name_series.iloc[i], "lat": lat_series.iloc[i], "lng": lng_series.iloc[i]})

    return locations

# Fetch locations
libraries_csv = pd.read_csv("Libraries.csv")
parks_csv = pd.read_csv("Parks.csv")
rec_centers_csv = pd.read_csv("Rec Center.csv")
soup_kitchens_csv = pd.read_csv("Soup Kitchens.csv")
bus_stops_csv = pd.read_csv("bus_stops.csv")
congregate_csv = pd.read_csv("Congregate Senior Dining Sites.csv")
housing_csv = pd.read_csv("Housing Resources.csv")
community_assistance_csv = pd.read_csv("community_centers_requested.csv")

housing = get_places_pandas(housing_csv["Lat"], housing_csv["Long"], housing_csv["Name"])
congregate = get_places_pandas(congregate_csv["Lat"], congregate_csv["Long"], congregate_csv["Name"])
community_assist = get_places_pandas(community_assistance_csv["Lat"], community_assistance_csv["Long"], community_assistance_csv["Name"])
libraries = get_places_pandas(libraries_csv['lat'], libraries_csv['lng'], libraries_csv['name'])
parks = get_places_pandas(parks_csv['lat'], parks_csv['lng'], parks_csv['name'])
rec_centers = get_places_pandas(rec_centers_csv['lat'], rec_centers_csv['lng'], rec_centers_csv['name'])
soup_kitchens = get_places_pandas(soup_kitchens_csv['lat'], soup_kitchens_csv['lng'], soup_kitchens_csv['name'])
bus_stops = get_places_pandas(bus_stops_csv['stop_lat'], bus_stops_csv['stop_lon'], bus_stops_csv['stop_name'])

#Save Google locations to .csv (ONCE/OLD)
#libraries.to_csv("Libraries.csv")
#parks.to_csv("Parks.csv")
#rec_centers.to_csv("Rec Center.csv")
#soup_kitchens.to_csv("Soup Kitchens.csv")'


# Define feature groups for different layers
layer_community = folium.FeatureGroup(name="Community Centers", show=False)
layer_libraries = folium.FeatureGroup(name="Libraries", show=False)
layer_parks_rec = folium.FeatureGroup(name="Parks & Recreation", show=False)
layer_food_assistance = folium.FeatureGroup(name="Food Assistance", show=False)
layer_transportation = folium.FeatureGroup(name="Transportation", show=False)
layer_housing = folium.FeatureGroup(name="Housing Assistance", show=False)

# Subgroups for more organization
libraries_layer = FeatureGroupSubGroup(layer_libraries, "Libraries")
community_assist_layer = FeatureGroupSubGroup(layer_community, "Community Assistance Centers")
parks_layer = FeatureGroupSubGroup(layer_parks_rec, "Parks")
rec_centers_layer = FeatureGroupSubGroup(layer_parks_rec, "Recreation Centers")
soup_layer = FeatureGroupSubGroup(layer_food_assistance, "Soup Kitchens")
dining_sites_layer = FeatureGroupSubGroup(layer_food_assistance, "Congregate Dining Sites")
bus_stops_layer = FeatureGroupSubGroup(layer_transportation, "Bus Stops")
housing_layer = FeatureGroupSubGroup(layer_housing, "Housing Assistance")


# Add places to layers
for place in libraries:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="blue", icon="book")
    ).add_to(libraries_layer)

for place in community_assist:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="cadetblue", icon="people-group", prefix="fa")
    ).add_to(community_assist_layer)

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

for place in congregate:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="gray", icon="utensils", prefix="fa")
    ).add_to(dining_sites_layer)

for place in bus_stops:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="lightblue", icon="bus", prefix="fa")
    ).add_to(bus_stops_layer)

for place in housing:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], parse_html=True),
        icon=folium.Icon(color="red", icon="house-chimney", prefix="fa")
    ).add_to(housing_layer)



# Add layers to map
m.add_child(layer_libraries)
layer_libraries.add_child(libraries_layer)

m.add_child(layer_community)
layer_community.add_child(community_assist_layer)

m.add_child(layer_parks_rec)
layer_parks_rec.add_child(parks_layer)
layer_parks_rec.add_child(rec_centers_layer)

m.add_child(layer_food_assistance)
layer_food_assistance.add_child(soup_layer)
layer_food_assistance.add_child(dining_sites_layer)

m.add_child(layer_transportation)
layer_transportation.add_child(bus_stops_layer)

m.add_child(layer_housing)
layer_housing.add_child(housing_layer)

# Add layer control to toggle visibility
folium.LayerControl(collapsed=False).add_to(m)

st.title("MSU Healthy City Assessment Map")
folium_static(m, width=700)
