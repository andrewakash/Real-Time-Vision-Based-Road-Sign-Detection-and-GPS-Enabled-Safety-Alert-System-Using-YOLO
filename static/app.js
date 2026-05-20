var firstLoad = true

// --------------------------------------------------
// MAP
// --------------------------------------------------

var map = L.map('map',{

    zoomControl:true,
    dragging:true,
    scrollWheelZoom:true,
    doubleClickZoom:true,
    touchZoom:true

}).setView(
    [11.5183,79.3256],
    13
)

L.tileLayer(

    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

    {

        attribution:'OpenStreetMap'

    }

).addTo(map)

// --------------------------------------------------
// VEHICLE MARKER
// --------------------------------------------------

var marker = L.marker(
    [11.5183,79.3256]
).addTo(map)

// --------------------------------------------------
// ROUTE LINE
// --------------------------------------------------

var polyline = L.polyline(
    [],
    {
        color:'lime',
        weight:5
    }
).addTo(map)

// --------------------------------------------------
// PLACE MARKERS
// --------------------------------------------------

window.placeMarkers = []

// --------------------------------------------------
// CHECKPOINT MARKERS
// --------------------------------------------------

window.checkpointMarkers = []

// --------------------------------------------------
// LOAD DASHBOARD
// --------------------------------------------------

async function loadDashboard(){

    const response = await fetch('/dashboard')

    const data = await response.json()

    // --------------------------------------------------
    // SPEED
    // --------------------------------------------------

    document.getElementById('speed').innerHTML =

        Math.round(data.speed)

    // --------------------------------------------------
    // WARNING
    // --------------------------------------------------

    document.getElementById('warning').innerHTML =

        data.warning

    if(data.warning == "SAFE"){

        document.getElementById('warning').className =

            "safe"

    }

    else{

        document.getElementById('warning').className =

            "danger"

    }

    // --------------------------------------------------
    // MAP LOCATION
    // --------------------------------------------------

    let newLatLng = L.latLng(

        data.lat,

        data.lon

    )

    // FIRST LOAD ONLY

    if(firstLoad){

        marker.setLatLng(newLatLng)

        map.setView(newLatLng,15)

        firstLoad = false
    }

    // AFTER FIRST LOAD

    else{

        marker.setLatLng(newLatLng)

    }

    // --------------------------------------------------
    // ROUTE LINE
    // --------------------------------------------------

    let routePoints = []

    for(let i=0;i<data.route.length;i++){

        routePoints.push([

            data.route[i].lat,

            data.route[i].lon

        ])

    }

    polyline.setLatLngs(routePoints)

    // --------------------------------------------------
    // REMOVE OLD PLACE MARKERS
    // --------------------------------------------------

    window.placeMarkers.forEach(m => {

        map.removeLayer(m)

    })

    window.placeMarkers = []

    // --------------------------------------------------
    // REMOVE OLD CHECKPOINTS
    // --------------------------------------------------

    window.checkpointMarkers.forEach(m => {

        map.removeLayer(m)

    })

    window.checkpointMarkers = []

    // --------------------------------------------------
    // PUBLIC PLACES
    // --------------------------------------------------

    let html = ""

    for(let i=0;i<data.places.length;i++){

        let p = data.places[i]

        html += `

        <li>

        ${p.type.toUpperCase()}

        →

        ${p.name}

        (${p.distance} km)

        </li>

        `

        // --------------------------------------------------
        // MAP PLACE MARKERS
        // --------------------------------------------------

        if(p.lat && p.lon){

            let placeMarker = L.marker(

                [p.lat,p.lon]

            ).addTo(map)

            placeMarker.bindPopup(

                `<b>${p.name}</b><br>${p.type}`

            )

            window.placeMarkers.push(placeMarker)

        }

    }

    document.getElementById(
        'places'
    ).innerHTML = html

    // --------------------------------------------------
    // CHECKPOINTS
    // --------------------------------------------------

    if(data.checkpoints){

        for(let i=0;i<data.checkpoints.length;i++){

            let cp = data.checkpoints[i]

            let cpMarker = L.circleMarker(

                [cp.lat,cp.lon],

                {

                    radius:8,
                    color:'yellow',
                    fillColor:'orange',
                    fillOpacity:1

                }

            ).addTo(map)

            cpMarker.bindPopup(

                "Checkpoint " + (i+1)

            )

            window.checkpointMarkers.push(cpMarker)

        }

    }

}

// --------------------------------------------------
// CAMERA DETECTION
// --------------------------------------------------

async function loadCamera(){

    const response = await fetch('/camera')

    const data = await response.json()

    document.getElementById(
        'cameraSign'
    ).innerHTML = data.sign

    document.getElementById(
        'warning'
    ).innerHTML = data.warning

    if(data.warning == "SAFE"){

        document.getElementById(
            'warning'
        ).className = "safe"

    }

    else{

        document.getElementById(
            'warning'
        ).className = "danger"

    }

}

// --------------------------------------------------
// START DRIVE
// --------------------------------------------------

async function startDrive(){

    await fetch('/start')

    alert("Tracking Started")

}

// --------------------------------------------------
// AUTO REFRESH
// --------------------------------------------------

setInterval(()=>{

    loadDashboard()

    loadCamera()

},2000)