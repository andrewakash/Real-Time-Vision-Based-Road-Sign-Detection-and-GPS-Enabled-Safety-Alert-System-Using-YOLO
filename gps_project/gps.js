function startGPS() {

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    const options = {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 5000
    };

    navigator.geolocation.watchPosition(
        function(position) {

            let lat = position.coords.latitude;
            let lon = position.coords.longitude;
            let speed = position.coords.speed;

            if (speed == null) {
                speed = 0;
            }

            let speed_kmh = speed * 3.6;

            document.getElementById("lat").innerText = lat;
            document.getElementById("lon").innerText = lon;
            document.getElementById("speed").innerText = speed_kmh.toFixed(2);

        },
        function(error) {
            alert("Location permission denied or unavailable");
        },
        options
    );
}