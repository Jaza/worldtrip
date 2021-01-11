var worldtrip = worldtrip || {};

worldtrip.location_map = function() {
    var $ = null;
    var map = null;
    var icon_url = null;

    function add_location_marker(k, loc) {
        var marker = L.marker(
            [loc.lat, loc.lon], {
                icon: L.icon({
                    iconUrl: icon_url,
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                }),
                title: loc.title})
            .addTo(map)
            .on('click', function(e) {
                window.location.href = loc.url;
            });
    }

    return {
        init: function(jq) {
            $ = jq;

            map = L.map('nodemap').setView([30.0, 0.0], 1);

            if (typeof mapbox_api_key !== 'undefined') {
                L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: 'mapbox/streets-v11',
                    tileSize: 512,
                    zoomOffset: -1,
                    accessToken: mapbox_api_key
                }).addTo(map);

                if (typeof countries !== 'undefined') {
                    icon_url = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png';
                    $.each(countries, add_location_marker);
                }
                if (typeof cities !== 'undefined') {
                    icon_url = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png';
                    $.each(cities, add_location_marker);
                }
            }
        }
    }
}();


jQuery(function() {
    worldtrip.location_map.init(jQuery);
});
