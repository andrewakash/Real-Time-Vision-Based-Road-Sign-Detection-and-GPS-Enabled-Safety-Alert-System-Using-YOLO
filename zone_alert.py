from zone_alert import *
import osmnx as ox
import folium
from geopy.distance import geodesic
import requests

# --------------------------------------------------
# STORE REAL DATA FOR FLASK
# --------------------------------------------------

places_data = []

zone_message = "SAFE"

# --------------------------------------------------
# GET CURRENT GPS LOCATION FROM YOUR FLASK SERVER
# --------------------------------------------------

def get_location():

    try:

        r = requests.get(
            "http://127.0.0.1:5000/location"
        )

        data = r.json()

        lat = float(data["lat"])
        lon = float(data["lon"])

        return (lat, lon)

    except:

        print("GPS not available. Using demo location.")

        return (10.7905, 78.7047)


vehicle_location = get_location()

print("\nVehicle Location:", vehicle_location)

# --------------------------------------------------
# BUILD ROAD GRAPH AROUND VEHICLE
# --------------------------------------------------

print("\nDownloading nearby road network...")

G = ox.graph_from_point(
    vehicle_location,
    dist=10000,
    network_type="drive"
)

# --------------------------------------------------
# GET ROUTE COORDINATES
# --------------------------------------------------

nodes = list(G.nodes)

route_coords = [
    (
        G.nodes[n]['y'],
        G.nodes[n]['x']
    )
    for n in nodes[:500]
]

# --------------------------------------------------
# CREATE CHECKPOINTS EVERY 2 KM
# --------------------------------------------------

checkpoints = [vehicle_location]

dist_accum = 0

for i in range(1, len(route_coords)):

    d = geodesic(
        route_coords[i-1],
        route_coords[i]
    ).km

    dist_accum += d

    if dist_accum >= 2:

        checkpoints.append(
            route_coords[i]
        )

        dist_accum = 0

    if len(checkpoints) == 6:
        break

# --------------------------------------------------
# FUNCTION TO GET PUBLIC AREAS
# --------------------------------------------------

def get_pois(point):

    try:

        tags = {
            "amenity": True
        }

        pois = ox.features_from_point(
            point,
            tags,
            dist=2000
        )

        if pois is None or len(pois) == 0:
            return []

        valid_types = [
            "school",
            "hospital",
            "clinic",
            "college"
        ]

        pois = pois[
            pois["amenity"].isin(valid_types)
        ]

        return pois.head(5)

    except:

        return []

# --------------------------------------------------
# ANALYZE CHECKPOINTS
# --------------------------------------------------

results = []

for i, pt in enumerate(checkpoints):

    pois = get_pois(pt)

    if len(pois) > 0:

        speed = "⚠ Slow down (30 km/h)"

        zone_message = "SLOW DOWN"

    else:

        speed = "Normal speed (50–60 km/h)"

        zone_message = "SAFE"

    names = []

    if len(pois) > 0:

        for _, row in pois.iterrows():

            name = str(row.get("name", "Unknown"))

            if name == "nan":

                name = "Unknown Place"

            typ = row.get(
                "amenity",
                "unknown"
            )
            

            distance = geodesic(
                vehicle_location,
                (
                    row.geometry.centroid.y,
                    row.geometry.centroid.x
                )
            ).km

            text = f"{typ.upper()} → {name}"

            names.append(text)

            # SAVE REAL DATA
            places_data.append({

    "name": name,

    "type": typ,

    "distance": round(distance, 2),

    "lat": float(
        row.geometry.centroid.y
    ),

    "lon": float(
        row.geometry.centroid.x
    )

})

    print("\n==============================")

    print(f"Checkpoint {i}")

    print("Location:", pt)

    print("Speed Advice:", speed)

    if names:

        print("Nearby Amenities:")

        for n in names:

            print("  -", n)

    else:

        print("No major amenities nearby")

    results.append((
        pt,
        speed,
        names
    ))

# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

print("\nGenerating map...")

m = folium.Map(
    location=vehicle_location,
    zoom_start=14
)

# VEHICLE MARKER

folium.Marker(

    vehicle_location,

    popup="🚗 Vehicle Location",

    icon=folium.Icon(
        color="blue",
        icon="car",
        prefix="fa"
    )

).add_to(m)

# CHECKPOINTS

for pt, speed, names in results:

    popup_text = speed

    if names:

        popup_text += "<br>" + "<br>".join(names)

    folium.Marker(

        location=pt,

        popup=folium.Popup(
            popup_text,
            max_width=300
        ),

        icon=folium.Icon(
            color="orange"
        )

    ).add_to(m)

# ROUTE LINES

for i in range(len(checkpoints)-1):

    folium.PolyLine(

        [
            checkpoints[i],
            checkpoints[i+1]
        ],

        color="green",

        weight=4

    ).add_to(m)

# SAVE MAP

m.save("map.html")

print("\n✅ Map saved as map.html")

# --------------------------------------------------
# SEND DATA TO FLASK
# --------------------------------------------------

def get_zone_data():

    return places_data, zone_message