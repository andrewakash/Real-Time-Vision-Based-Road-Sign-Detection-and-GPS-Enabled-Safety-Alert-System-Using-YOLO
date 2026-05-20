latest_sign = "NO SIGN"
latest_warning = "SAFE"

from detect_web import get_detection
from zone_alert import get_zone_data

import json
import time

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# LIVE GPS
# --------------------------------------------------

latest_location = {

    "lat": 11.5183,
    "lon": 79.3256
}

# --------------------------------------------------
# CURRENT SPEED
# --------------------------------------------------

current_speed = 0

# --------------------------------------------------
# PREVIOUS GPS
# --------------------------------------------------

previous_point = None
previous_time = None

# --------------------------------------------------
# ROUTE STORAGE
# --------------------------------------------------

route_history = []

tracking_enabled = False

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")

# --------------------------------------------------
# GPS PAGE
# --------------------------------------------------

@app.route("/gpspage")
def gpspage():

    return render_template("gps.html")

# --------------------------------------------------
# RECEIVE GPS
# --------------------------------------------------

@app.route("/gps")
def gps():

    global previous_point
    global previous_time
    global current_speed
    global route_history

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:

        lat = float(lat)
        lon = float(lon)

        latest_location["lat"] = lat
        latest_location["lon"] = lon

        current_point = (lat, lon)

        current_time = time.time()

        # --------------------------------------------------
        # SPEED CALCULATION
        # --------------------------------------------------

        if previous_point is not None:

            distance = geodesic(

                previous_point,
                current_point

            ).meters

            time_diff = current_time - previous_time

            if time_diff > 0:

                speed_mps = distance / time_diff

                current_speed = speed_mps * 3.6

        previous_point = current_point
        previous_time = current_time

        # --------------------------------------------------
        # SAVE ROUTE
        # --------------------------------------------------

        if tracking_enabled:

            route_history.append({

                "lat": lat,
                "lon": lon
            })

            if len(route_history) > 100:

                route_history.pop(0)

            with open("route.json", "w") as file:

                json.dump(route_history, file)

        print("\n========================")
        print("📍 GPS RECEIVED")
        print("Latitude :", lat)
        print("Longitude:", lon)

        print(
            "🚗 Current Speed:",
            round(current_speed, 2),
            "km/h"
        )

    return "OK"

# --------------------------------------------------
# SEND LOCATION
# --------------------------------------------------

@app.route("/location")
def location():

    return jsonify({

        "lat": latest_location["lat"],
        "lon": latest_location["lon"]
    })

# --------------------------------------------------
# SEND SPEED
# --------------------------------------------------

@app.route("/speed")
def speed():

    return jsonify({

        "speed": round(current_speed, 2)
    })

# --------------------------------------------------
# START DRIVE
# --------------------------------------------------

@app.route("/start")
def start():

    global tracking_enabled
    global route_history

    tracking_enabled = True

    route_history = []

    print("\n▶ Tracking Started")

    return "Tracking Started"

# --------------------------------------------------
# STOP DRIVE
# --------------------------------------------------

@app.route("/stop")
def stop():

    global tracking_enabled

    tracking_enabled = False

    print("\n⏹ Tracking Stopped")

    return "Tracking Stopped"

# --------------------------------------------------
# SEND ROUTE
# --------------------------------------------------

@app.route("/route")
def route():

    return jsonify(route_history)

# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    # --------------------------------------------------
    # GET PUBLIC PLACES
    # --------------------------------------------------

    try:

        public_places, zone_message = get_zone_data()

    except Exception as e:

        print(e)

        public_places = []

        zone_message = "SAFE"

    # --------------------------------------------------
    # CAMERA DETECTION
    # --------------------------------------------------

    try:

        sign, camera_warning = get_detection()

    except:

        sign = "NO SIGN"

        camera_warning = "SAFE"

    # --------------------------------------------------
    # FINAL WARNING
    # --------------------------------------------------

    if current_speed > 30:

        final_warning = "DANGER"

    elif camera_warning != "SAFE":

        final_warning = camera_warning

    else:

        final_warning = "SAFE"

    # --------------------------------------------------
    # CHECKPOINTS
    # --------------------------------------------------

    checkpoints = []

    for i in range(0, len(route_history), 5):

        checkpoints.append({

            "lat": route_history[i]["lat"],
            "lon": route_history[i]["lon"]

        })

    # --------------------------------------------------
    # SEND JSON
    # --------------------------------------------------

    return jsonify({

        "lat": latest_location["lat"],

        "lon": latest_location["lon"],

        "speed": round(current_speed, 2),

        "sign": sign,

        "warning": final_warning,

        "route": route_history,

        "places": public_places,

        "checkpoints": checkpoints
    })

# --------------------------------------------------
# CAMERA API
# --------------------------------------------------

@app.route("/camera")
def camera():

    sign, warning = get_detection()

    return jsonify({

        "sign": sign,
        "warning": warning
    })

# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

app.run(

    host="0.0.0.0",
    port=5000
)